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

const (
	IDAvatarAres  = 100
	IDSpinner     = 200
	IDAvatarUser  = 300
	IDSeparator   = 400
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
	dLog = log.New(f, "[FÍSICA_ARES] ", log.LstdFlags|log.Lshortfile)
}

func logStep(msg string, v ...interface{}) {
	if dLog != nil { dLog.Printf(msg, v...) }
}

func getTermSize() (cellW, cellH int) {
	ws, err := unix.IoctlGetWinsize(int(os.Stdout.Fd()), unix.TIOCGWINSZ)
	if err != nil || ws.Col == 0 { return 10, 20 }
	return int(ws.Xpixel / ws.Col), int(ws.Ypixel / ws.Row)
}

func resizeImage(src image.Image, w, h int) image.Image {
	dst := image.NewRGBA(image.Rect(0, 0, w, h))
	sb := src.Bounds()
	sW, sH := sb.Dx(), sb.Dy()
	if sW == 0 || sH == 0 { return dst }
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			dst.Set(x, y, src.At(x*sW/w, y*sH/h))
		}
	}
	return dst
}

func transmitViaFile(cmd string, data []byte) {
	tmpFile, err := os.CreateTemp("", TempPrefix+"*.png")
	if err != nil { return }
	defer tmpFile.Close()
	tmpFile.Write(data)
	pathB64 := base64.StdEncoding.EncodeToString([]byte(tmpFile.Name()))
	fmt.Printf("\033_G%s,t=t,q=2;%s\033\\", cmd, pathB64)
}

func processGIF(path string, cfg AssetConfig, id uint32, loop int, cW, cH int) {
	f, _ := os.Open(path)
	defer f.Close()
	g, _ := gif.DecodeAll(f)
	targetW, targetH := cfg.Width*cW, cfg.Height*cH
	canvas := image.NewRGBA(g.Image[0].Bounds())
	for i, frame := range g.Image {
		draw.Draw(canvas, frame.Bounds(), frame, frame.Bounds().Min, draw.Over)
		resized := resizeImage(canvas, targetW, targetH)
		var buf bytes.Buffer
		png.Encode(&buf, resized)
		if i == 0 {
			transmitViaFile(fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex), buf.Bytes())
		} else {
			delay := g.Delay[i] * 10
			if delay == 0 { delay = 100 }
			transmitViaFile(fmt.Sprintf("a=f,i=%d,f=100,r=%d,z=%d", id, i+1, delay), buf.Bytes())
		}
	}
	lv := loop
	if lv < 0 { lv = 0 }
	fmt.Printf("\033_Ga=a,i=%d,s=3,v=%d,q=2\033\\", id, lv)
}

func renderAsset(path string, cfg AssetConfig, id uint32, loop int) {
	if _, err := os.Stat(path); err != nil { return }
	cW, cH := getTermSize()
	fmt.Printf("\033_Ga=d,d=i,i=%d,q=2\033\\", id)
	fmt.Printf("\033[%d;%dH", cfg.Y+1, cfg.X+1)
	if filepath.Ext(path) == ".gif" {
		processGIF(path, cfg, id, loop, cW, cH)
	} else {
		f, _ := os.Open(path)
		defer f.Close()
		img, _, _ := image.Decode(f)
		resized := resizeImage(img, cfg.Width*cW, cfg.Height*cH)
		var buf bytes.Buffer
		png.Encode(&buf, resized)
		transmitViaFile(fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex), buf.Bytes())
	}
}

func main() {
	currDir, _ := os.Getwd()
	initLogger(currDir)
	mode := flag.String("mode", "ares", "Modo")
	spinner := flag.Bool("spinner", false, "Spinner")
	rotate := flag.Bool("rotate", false, "Rotar")
	stype := flag.String("type", "ares", "Tipo")
	espacios := flag.Int("espacios", 0, "Espacios")
	configPath := flag.String("config", "config.yaml", "Config")
	flag.Parse()

	if *mode == "space" {
		for i := 0; i < *espacios; i++ { fmt.Println() }
		return
	}

	cData, _ := os.ReadFile(*configPath)
	var cfg Config
	yaml.Unmarshal(cData, &cfg)
	os.MkdirAll(cfg.Cache.Dir, 0755)
	stateFile := filepath.Join(cfg.Cache.Dir, ".spinner_state.json")

	switch *mode {
	case "ares":
		renderAsset(cfg.Ares.Avatar.Path, cfg.Ares.Avatar, IDAvatarAres, 0)
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
			}
			sCfg := AssetConfig{
				Path: cfg.Ares.Spinner.List[idx], Width: cfg.Ares.Spinner.Width,
				Height: cfg.Ares.Spinner.Height, X: cfg.Ares.Spinner.X, Y: cfg.Ares.Spinner.Y,
				ZIndex: cfg.Ares.Spinner.ZIndex,
			}
			renderAsset(sCfg.Path, sCfg, IDSpinner, cfg.Ares.Anim.Loop)
		}
	case "user":
		renderAsset(cfg.User.Avatar.Path, cfg.User.Avatar, IDAvatarUser, 0)
	case "separator":
		if asset, ok := cfg.Separators[*stype]; ok {
			renderAsset(asset.Path, asset, IDSeparator, cfg.Ares.Anim.Loop)
		}
	}
	fmt.Print("\n\n\n")
}
