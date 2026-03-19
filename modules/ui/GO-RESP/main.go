package main

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"image"
	"image/draw"
	"image/gif"
	"image/png"
	"log"
	"os"
	"path/filepath"

	"golang.org/x/sys/unix"
	"gopkg.in/yaml.v3"
)

// --- CONSTANTES DE PROTOCOLO ---
const (
	KittyIDAvatar  = 100
	KittyIDSpinner = 200
	TempPrefix     = "tty-graphics-protocol-ares-"
)

// --- TIPOS ---

type Config struct {
	Ares struct {
		Avatar  AssetConfig   `yaml:"avatar"`
		Spinner SpinnerConfig `yaml:"spinner"`
		Anim    AnimConfig    `yaml:"anim"`
	} `yaml:"ares"`
	Cache struct {
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

var debugLog *log.Logger

// --- MÓDULO: DEPURACIÓN FOCALIZADA ---

func initLogger(dir string) {
	logPath := filepath.Join(dir, "debug.log")
	f, _ := os.OpenFile(logPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	debugLog = log.New(f, "[FÍSICA_ARES] ", log.LstdFlags|log.Lshortfile)
	debugLog.Println("\n=== INVESTIGACIÓN DE BAJO NIVEL: OPTIMIZACIÓN DE CARGA ===")
}

// --- MÓDULO: TERMINAL (GEOMETRÍA) ---

func getTermSize() (cellW, cellH int) {
	ws, err := unix.IoctlGetWinsize(int(os.Stdout.Fd()), unix.TIOCGWINSZ)
	if err != nil || ws.Col == 0 {
		debugLog.Printf("ERROR: No se pudo obtener TIOCGWINSZ, usando fallbacks")
		return 10, 20
	}
	cellW = int(ws.Xpixel / ws.Col)
	cellH = int(ws.Ypixel / ws.Row)
	debugLog.Printf("GEOMETRÍA: CellSize=%dx%d pixels (TermSize=%dx%d)", cellW, cellH, ws.Xpixel, ws.Ypixel)
	return
}

// --- MÓDULO: PROCESADOR DE IMAGEN (ANTI-PIXELACIÓN) ---

func resizeImage(src image.Image, w, h int) image.Image {
	dst := image.NewRGBA(image.Rect(0, 0, w, h))
	// Box scaling manual para evitar pixelación sin dependencias externas
	srcBounds := src.Bounds()
	srcW := srcBounds.Dx()
	srcH := srcBounds.Dy()
	
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			srcX := x * srcW / w
			srcY := y * srcH / h
			dst.Set(x, y, src.At(srcX, srcY))
		}
	}
	return dst
}

// --- MÓDULO: PROTOCOLO KGP (OPTIMIZADO t=t) ---

func transmitViaFile(cmd string, data []byte) {
	tmpFile, err := os.CreateTemp("", TempPrefix+"*.png")
	if err != nil {
		debugLog.Printf("ERROR: Falló creación de tmp: %v", err)
		return
	}
	defer tmpFile.Close()
	
	tmpFile.Write(data)
	pathB64 := base64.StdEncoding.EncodeToString([]byte(tmpFile.Name()))
	
	sequence := fmt.Sprintf("\033_G%s,t=t,q=2;%s\033\\", cmd, pathB64)
	fmt.Print(sequence)
}

// --- MÓDULO: GESTOR DE GIFS ---

func processGIF(path string, cfg AssetConfig, id uint32, loop int, cW, cH int) {
	f, _ := os.Open(path)
	defer f.Close()
	g, err := gif.DecodeAll(f)
	if err != nil { return }

	targetW := cfg.Width * cW
	targetH := cfg.Height * cH
	
	debugLog.Printf("GIF_PROCESS: %s -> TargetPixels=%dx%d", path, targetW, targetH)
	
	canvas := image.NewRGBA(g.Image[0].Bounds())
	
	for i, frame := range g.Image {
		draw.Draw(canvas, frame.Bounds(), frame, frame.Bounds().Min, draw.Over)
		
		resizedFrame := resizeImage(canvas, targetW, targetH)
		
		var buf bytes.Buffer
		png.Encode(&buf, resizedFrame)

		if i == 0 {
			cmd := fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex)
			transmitViaFile(cmd, buf.Bytes())
		} else {
			delay := g.Delay[i] * 10
			if delay == 0 { delay = 100 }
			cmd := fmt.Sprintf("a=f,i=%d,f=100,r=%d,z=%d", id, i+1, delay)
			transmitViaFile(cmd, buf.Bytes())
		}
	}
	
	loopVal := loop
	if loopVal < 0 { loopVal = 0 }
	fmt.Printf("\033_Ga=a,i=%d,s=3,v=%d,q=2\033\\", id, loopVal)
	debugLog.Printf("GIF_READY: %d frames cargados mediante t=t", len(g.Image))
}

func renderAsset(path string, cfg AssetConfig, id uint32, loop int) {
	cW, cH := getTermSize()
	
	fmt.Printf("\033_Ga=d,d=i,i=%d,q=2\033\\", id)
	fmt.Printf("\033[%d;%dH", cfg.Y+1, cfg.X+1)
	
	if filepath.Ext(path) == ".gif" {
		processGIF(path, cfg, id, loop, cW, cH)
	} else {
		srcFile, _ := os.Open(path)
		defer srcFile.Close()
		img, _, _ := image.Decode(srcFile)
		
		targetW := cfg.Width * cW
		targetH := cfg.Height * cH
		resized := resizeImage(img, targetW, targetH)
		
		var buf bytes.Buffer
		png.Encode(&buf, resized)
		
		cmd := fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex)
		transmitViaFile(cmd, buf.Bytes())
	}
}

func main() {
	currentDir, _ := os.Getwd()
	initLogger(currentDir)
	
	mode := flag.String("mode", "ares", "Modo")
	rotate := flag.Bool("rotate", false, "Rotar")
	configPath := flag.String("config", "config.yaml", "Config")
	flag.Parse()

	cfgData, _ := os.ReadFile(*configPath)
	var cfg Config
	yaml.Unmarshal(cfgData, &cfg)

	stateFile := filepath.Join(cfg.Cache.Dir, ".spinner_state.json")
	os.MkdirAll(cfg.Cache.Dir, 0755)

	if *mode == "ares" {
		renderAsset(cfg.Ares.Avatar.Path, cfg.Ares.Avatar, KittyIDAvatar, 0)
		
		total := len(cfg.Ares.Spinner.List)
		if total > 0 {
			var state struct{ Idx int }
			sData, _ := os.ReadFile(stateFile)
			json.Unmarshal(sData, &state)
			idx := state.Idx % total
			
			if *rotate {
				idx = (idx + 1) % total
				state.Idx = idx
				res, _ := json.Marshal(state)
				os.WriteFile(stateFile, res, 0644)
			}
			
			spinnerPath := cfg.Ares.Spinner.List[idx]
			spinnerCfg := AssetConfig{
				Path: spinnerPath, Width: cfg.Ares.Spinner.Width, Height: cfg.Ares.Spinner.Height,
				X: cfg.Ares.Spinner.X, Y: cfg.Ares.Spinner.Y, ZIndex: cfg.Ares.Spinner.ZIndex,
			}
			renderAsset(spinnerPath, spinnerCfg, KittyIDSpinner, cfg.Ares.Anim.Loop)
		}
	}
	fmt.Print("\n\n\n")
	debugLog.Println("Ciclo completado.")
}
