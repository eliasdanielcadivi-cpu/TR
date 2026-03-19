package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"image"
	_ "image/gif"
	_ "image/jpeg"
	_ "image/png"
	"image/draw"
	"image/gif"
	"image/png"
	"log"
	"os"
	"path/filepath"

	"golang.org/x/sys/unix"
	"gopkg.in/yaml.v3"
)

// --- CONSTANTES CRÍTICAS ---
const (
	IDAvatarAres  = 100
	IDSpinner     = 200
	IDAvatarUser  = 300
	IDSeparator   = 400
	// EL PREFIJO DEBE CONTENER 'tty-graphics-protocol' O KITTY LO RECHAZA
	TempPrefix    = "tty-graphics-protocol-ares-"
)

type Config struct {
	Ares struct {
		Avatar  AssetConfig   `yaml:"avatar"`
		Spinner SpinnerConfig `yaml:"spinner"`
		Anim    AnimConfig    `yaml:"anim"`
	} `yaml:"ares"`
	User struct {
		Avatar AssetConfig `yaml:"avatar"`
	} `yaml:"user"`
	Separators map[string]AssetConfig `yaml:"separators"`
	Cache      struct {
		Dir string `yaml:"dir"`
	} `yaml:"cache"`
}

type AssetConfig struct {
	Path   string `yaml:"path"`
	Width  int    `yaml:"width"`
	Height int    `yaml:"height"`
	X      int    `yaml:"x"`
	Y      int    `yaml:"y"`
	ZIndex int    `yaml:"z_index"`
}

type SpinnerConfig struct {
	List   []string `yaml:"list"`
	Width  int      `yaml:"width"`
	Height int      `yaml:"height"`
	X      int      `yaml:"x"`
	Y      int      `yaml:"y"`
	ZIndex int      `yaml:"z_index"`
}

type AnimConfig struct {
	Loop int `yaml:"loop"`
}

var dLog *log.Logger

func initLogger(dir string) {
	logPath := filepath.Join(dir, "debug.log")
	f, _ := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	dLog = log.New(f, "[MAX_DEBUG] ", log.LstdFlags|log.Lshortfile)
	dLog.Println("\n>>> ANALIZANDO FISICA DE TERMINAL Y CARGA <<<")
}

func logV(tag string, msg string, v ...interface{}) {
	if dLog != nil { dLog.Printf("[%s] "+msg, append([]interface{}{tag}, v...)...) }
}

func getTermSize() (cW, cH int) {
	ws, err := unix.IoctlGetWinsize(int(os.Stdout.Fd()), unix.TIOCGWINSZ)
	if err != nil || ws.Col == 0 {
		logV("TERM", "Error TIOCGWINSZ, usando defaults 10x20")
		return 10, 20
	}
	cW, cH = int(ws.Xpixel/ws.Col), int(ws.Ypixel/ws.Row)
	logV("TERM", "Celda Detectada: %dx%d (Total Px: %dx%d)", cW, cH, ws.Xpixel, ws.Ypixel)
	return
}

func resizeBox(src image.Image, w, h int) image.Image {
	dst := image.NewRGBA(image.Rect(0, 0, w, h))
	srcB := src.Bounds()
	sW, sH := srcB.Dx(), srcB.Dy()
	if sW == 0 || sH == 0 { return dst }
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			dst.Set(x, y, src.At(x*sW/w, y*sH/h))
		}
	}
	return dst
}

func transmit(cmd string, data []byte) {
	tmp, err := os.CreateTemp("", TempPrefix+"*.png")
	if err != nil {
		logV("IO", "ERROR CREANDO TMP: %v", err)
		return
	}
	defer tmp.Close()
	tmp.Write(data)
	pathB64 := base64.StdEncoding.EncodeToString([]byte(tmp.Name()))
	
	logV("KGP", "Enviando Escape: cmd={%s} path={%s}", cmd, tmp.Name())
	fmt.Printf("\033_G%s,t=t,q=2;%s\033\\", cmd, pathB64)
}

func render(path string, cfg AssetConfig, id uint32, loop int) {
	logV("RENDER", "Iniciando: %s ID=%d Pos=%d,%d", path, id, cfg.X, cfg.Y)
	
	if _, err := os.Stat(path); err != nil {
		logV("RENDER", "ERROR: Archivo no accesible: %v", err)
		return
	}

	cW, cH := getTermSize()
	tW, tH := cfg.Width*cW, cfg.Height*cH
	
	// Limpieza y posicionamiento
	fmt.Printf("\033_Ga=d,d=i,i=%d,q=2\033\\", id)
	fmt.Printf("\033[%d;%dH", cfg.Y+1, cfg.X+1)

	if filepath.Ext(path) == ".gif" {
		f, _ := os.Open(path)
		defer f.Close()
		g, err := gif.DecodeAll(f)
		if err != nil {
			logV("GIF", "Error DecodeAll: %v", err)
			return
		}
		
		logV("GIF", "Decodificados %d frames", len(g.Image))
		canvas := image.NewRGBA(g.Image[0].Bounds())
		for i, frame := range g.Image {
			draw.Draw(canvas, frame.Bounds(), frame, frame.Bounds().Min, draw.Over)
			resized := resizeBox(canvas, tW, tH)
			var buf bytes.Buffer
			png.Encode(&buf, resized)
			
			if i == 0 {
				// Base: a=T con dimensiones y z-index
				cmd := fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex)
				transmit(cmd, buf.Bytes())
			} else {
				// Frames: a=f con número de frame y gap (delay)
				delay := g.Delay[i] * 10
				if delay == 0 { delay = 100 }
				cmd := fmt.Sprintf("a=f,i=%d,f=100,r=%d,z=%d", id, i+1, delay)
				transmit(cmd, buf.Bytes())
			}
		}
		lv := loop
		if lv < 0 { lv = 0 }
		fmt.Printf("\033_Ga=a,i=%d,s=3,v=%d,q=2\033\\", id, lv)
		logV("ANIM", "Animación disparada loop=%d", lv)
	} else {
		f, _ := os.Open(path)
		defer f.Close()
		img, _, err := image.Decode(f)
		if err != nil {
			logV("IMG", "Error Decode estático (%s): %v", path, err)
			return
		}
		resized := resizeBox(img, tW, tH)
		var buf bytes.Buffer
		png.Encode(&buf, resized)
		cmd := fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex)
		transmit(cmd, buf.Bytes())
		logV("IMG", "Estático enviado.")
	}
}

func main() {
	currDir, _ := os.Getwd()
	initLogger(currDir)
	
	mode := flag.String("mode", "ares", "ares, user, separator, space")
	spinner := flag.Bool("spinner", false, "Mostrar spinner")
	rotate := flag.Bool("rotate", false, "Rotar lista")
	stype := flag.String("type", "ares", "Tipo separador")
	espacios := flag.Int("espacios", 0, "N retornos")
	config := flag.String("config", "config.yaml", "Ruta YAML")
	flag.Parse()

	logV("MAIN", "MODO=%s SPINNER=%v ROTATE=%v", *mode, *spinner, *rotate)

	if *mode == "space" {
		for i := 0; i < *espacios; i++ { fmt.Println() }
		return
	}

	data, err := os.ReadFile(*config)
	if err != nil {
		logV("YAML", "FATAL: No existe config.yaml")
		return
	}
	var cfg Config
	yaml.Unmarshal(data, &cfg)

	stateFile := filepath.Join(cfg.Cache.Dir, ".spinner_state.json")
	os.MkdirAll(cfg.Cache.Dir, 0755)

	switch *mode {
	case "ares":
		render(cfg.Ares.Avatar.Path, cfg.Ares.Avatar, IDAvatarAres, 0)
		if *spinner && len(cfg.Ares.Spinner.List) > 0 {
			var st struct{ Idx int }
			sData, _ := os.ReadFile(stateFile)
			json.Unmarshal(sData, &st)
			idx := st.Idx % len(cfg.Ares.Spinner.List)
			if *rotate {
				idx = (idx + 1) % len(cfg.Ares.Spinner.List)
				st.Idx = idx
				res, _ := json.Marshal(st)
				os.WriteFile(stateFile, res, 0644)
				logV("ROTATE", "Nuevo Indice: %d", idx)
			}
			render(cfg.Ares.Spinner.List[idx], AssetConfig{
				Path: cfg.Ares.Spinner.List[idx], Width: cfg.Ares.Spinner.Width,
				Height: cfg.Ares.Spinner.Height, X: cfg.Ares.Spinner.X, Y: cfg.Ares.Spinner.Y,
				ZIndex: cfg.Ares.Spinner.ZIndex,
			}, IDSpinner, cfg.Ares.Anim.Loop)
		}
	case "user":
		render(cfg.User.Avatar.Path, cfg.User.Avatar, IDAvatarUser, 0)
	case "separator":
		if asset, ok := cfg.Separators[*stype]; ok {
			render(asset.Path, asset, IDSeparator, cfg.Ares.Anim.Loop)
		} else {
			logV("SEP", "ERROR: Tipo %s no hallado en YAML", *stype)
		}
	}
	fmt.Print("\n\n\n")
	logV("MAIN", "Finalizado.")
}
