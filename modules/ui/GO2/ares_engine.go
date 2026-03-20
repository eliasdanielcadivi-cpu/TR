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
	"os"
	"path/filepath"

	"golang.org/x/sys/unix"
	"gopkg.in/yaml.v3"
)

// IDs únicos para que no se borren entre sí en la pantalla
const (
	IDAvatar   = 100
	IDSpinner  = 200
	IDFooter   = 300
	IDUser     = 400
	IDAnimAres = 500
	TempPrefix = "tty-graphics-protocol-ares-"
)

type AssetConfig struct {
	Path   string `yaml:"path"`
	Width  int    `yaml:"width"`
	Height int    `yaml:"height"`
	X      int    `yaml:"x"`
	Y      int    `yaml:"y"`
	ZIndex int    `yaml:"z_index"`
}

type Config struct {
	Ares struct {
		Avatar  AssetConfig `yaml:"avatar"`
		Spinner struct {
			List   []string `yaml:"list"`
			Width  int      `yaml:"width"`
			Height int      `yaml:"height"`
			X      int      `yaml:"x"`
			Y      int      `yaml:"y"`
			ZIndex int      `yaml:"z_index"`
		} `yaml:"spinner"`
		Footer   AssetConfig `yaml:"footer"`
		AresAnim AssetConfig `yaml:"ares_anim"`
		Anim     struct { Loop int `yaml:"loop"` } `yaml:"anim"`
	} `yaml:"ares"`
	User struct {
		Avatar AssetConfig `yaml:"avatar"`
	} `yaml:"user"`
	Cache struct { Dir string `yaml:"dir"` } `yaml:"cache"`
}

func getTermSize() (cellW, cellH int) {
	ws, err := unix.IoctlGetWinsize(int(os.Stdout.Fd()), unix.TIOCGWINSZ)
	if err != nil || ws.Col == 0 { return 10, 20 }
	return int(ws.Xpixel / ws.Col), int(ws.Ypixel / ws.Row)
}

func resizeImage(src image.Image, w, h int) image.Image {
	dst := image.NewRGBA(image.Rect(0, 0, w, h))
	srcBounds := src.Bounds()
	if srcBounds.Dx() == 0 || srcBounds.Dy() == 0 { return dst }
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			dst.Set(x, y, src.At(x*srcBounds.Dx()/w, y*srcBounds.Dy()/h))
		}
	}
	return dst
}

func transmitViaFile(cmd string, data []byte) {
	tmpFile, _ := os.CreateTemp("", TempPrefix+"*.png")
	defer tmpFile.Close()
	tmpFile.Write(data)
	pathB64 := base64.StdEncoding.EncodeToString([]byte(tmpFile.Name()))
	fmt.Printf("\033_G%s,t=t,q=2;%s\033\\", cmd, pathB64)
}

func renderAsset(path string, cfg AssetConfig, id uint32, loop int) {
	if _, err := os.Stat(path); err != nil { return }
	cW, cH := getTermSize()
	fmt.Printf("\033[%d;%dH", cfg.Y+1, cfg.X+1)
	
	if filepath.Ext(path) == ".gif" {
		f, _ := os.Open(path)
		g, _ := gif.DecodeAll(f)
		f.Close()
		targetW, targetH := cfg.Width*cW, cfg.Height*cH
		canvas := image.NewRGBA(g.Image[0].Bounds())
		
		for i, frame := range g.Image {
			draw.Draw(canvas, frame.Bounds(), frame, frame.Bounds().Min, draw.Over)
			resized := resizeImage(canvas, targetW, targetH)
			var buf bytes.Buffer
			png.Encode(&buf, resized)
			if i == 0 {
				transmit(fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex), buf.Bytes())
			} else {
				delay := g.Delay[i] * 10
				if delay == 0 { delay = 100 }
				transmit(fmt.Sprintf("a=f,i=%d,f=100,r=%d,z=%d", id, i+1, delay), buf.Bytes())
			}
		}
		lv := loop
		if lv < 0 { lv = 0 }
		fmt.Printf("\033_Ga=a,i=%d,s=3,v=%d,q=2\033\\", id, lv)
	} else {
		f, _ := os.Open(path)
		img, _, _ := image.Decode(f)
		f.Close()
		resized := resizeImage(img, cfg.Width*cW, cfg.Height*cH)
		var buf bytes.Buffer
		png.Encode(&buf, resized)
		transmit(fmt.Sprintf("a=T,i=%d,f=100,c=%d,r=%d,z=%d", id, cfg.Width, cfg.Height, cfg.ZIndex), buf.Bytes())
	}
}

func transmit(cmd string, data []byte) { transmitViaFile(cmd, data) }

func main() {
	mode := flag.String("mode", "", "avatar|spinner|footer|user|anim")
	rotate := flag.Bool("rotate", false, "rotar index")
	configPath := flag.String("config", "config.yaml", "path")
	flag.Parse()

	if *mode == "" { flag.Usage(); return }

	cfgData, _ := os.ReadFile(*configPath)
	var cfg Config
	yaml.Unmarshal(cfgData, &cfg)

	switch *mode {
	case "avatar":
		renderAsset(cfg.Ares.Avatar.Path, cfg.Ares.Avatar, IDAvatar, 0)
	case "spinner":
		total := len(cfg.Ares.Spinner.List)
		if total == 0 { return }
		cacheDir := cfg.Cache.Dir
		if cacheDir == "" { cacheDir = "cache" }
		os.MkdirAll(cacheDir, 0755)
		stateFile := filepath.Join(cacheDir, ".spinner_state.json")
		var state struct{ Idx int }
		if sData, err := os.ReadFile(stateFile); err == nil {
			json.Unmarshal(sData, &state)
		}
		if *rotate {
			state.Idx = (state.Idx + 1) % total
			res, _ := json.Marshal(state)
			os.WriteFile(stateFile, res, 0644)
		}
		sCfg := AssetConfig{Path: cfg.Ares.Spinner.List[state.Idx % total], Width: cfg.Ares.Spinner.Width, Height: cfg.Ares.Spinner.Height, X: cfg.Ares.Spinner.X, Y: cfg.Ares.Spinner.Y, ZIndex: cfg.Ares.Spinner.ZIndex}
		renderAsset(sCfg.Path, sCfg, IDSpinner, cfg.Ares.Anim.Loop)
	case "footer":
		renderAsset(cfg.Ares.Footer.Path, cfg.Ares.Footer, IDFooter, cfg.Ares.Anim.Loop)
	case "user":
		renderAsset(cfg.User.Avatar.Path, cfg.User.Avatar, IDUser, 0)
	case "anim":
		renderAsset(cfg.Ares.AresAnim.Path, cfg.Ares.AresAnim, IDAnimAres, cfg.Ares.Anim.Loop)
	}
	fmt.Print("\n\n\n")
}
