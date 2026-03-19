# maestro.md - Contenido de: /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo

**Extensiones procesadas:** `.go`

## /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo/main.go

```
// License: GPLv3 Copyright: 2022, Kovid Goyal, <kovid at kovidgoyal.net>

package icat

import (
	"fmt"
	"math"
	"os"
	"runtime"
	"slices"
	"strconv"
	"strings"
	"sync/atomic"
	"time"

	"github.com/kovidgoyal/imaging"
	"github.com/kovidgoyal/kitty/tools/cli"
	"github.com/kovidgoyal/kitty/tools/tty"
	"github.com/kovidgoyal/kitty/tools/tui"
	"github.com/kovidgoyal/kitty/tools/tui/graphics"
	"github.com/kovidgoyal/kitty/tools/utils"
	"github.com/kovidgoyal/kitty/tools/utils/style"

	"golang.org/x/sys/unix"
)

var _ = fmt.Print

type Place struct {
	width, height, left, top int
}

var opts *Options
var place *Place
var z_index int32
var remove_alpha *imaging.NRGBColor
var flip, flop bool

type transfer_mode int

const (
	unknown transfer_mode = iota
	unsupported
	supported
)

type fit_t int

const (
	fit_none fit_t = iota
	fit_width
	fit_height
	fit_both
)

var transfer_by_file, transfer_by_memory transfer_mode

var files_channel chan input_arg
var output_channel chan *image_data
var num_of_items int
var keep_going *atomic.Bool
var screen_size *unix.Winsize
var fit_mode fit_t

func send_output(imgd *image_data) {
	output_channel <- imgd
}

func parse_mirror() (err error) {
	flip = opts.Mirror == "both" || opts.Mirror == "vertical"
	flop = opts.Mirror == "both" || opts.Mirror == "horizontal"
	return
}

func parse_background() (err error) {
	if opts.Background == "" || opts.Background == "none" {
		return nil
	}
	col, err := style.ParseColor(opts.Background)
	if err != nil {
		return fmt.Errorf("Invalid value for --background: %w", err)
	}
	remove_alpha = &imaging.NRGBColor{R: col.Red, G: col.Green, B: col.Blue}
	return
}

func parse_z_index() (err error) {
	val := opts.ZIndex
	var origin int32
	if strings.HasPrefix(val, "--") {
		origin = -1073741824
		val = val[1:]
	}
	i, err := strconv.ParseInt(val, 10, 32)
	if err != nil {
		return fmt.Errorf("Invalid value for --z-index with error: %w", err)
	}
	z_index = int32(i) + origin
	return
}

func parse_fit() (err error) {
	switch strings.ToLower(opts.Fit) {
	case "width":
		fit_mode = fit_width
	case "height":
		fit_mode = fit_height
	case "none", "neither":
		fit_mode = fit_none
	case "both":
		fit_mode = fit_both
	default:
		return fmt.Errorf("unknown fit specification: %#v", opts.Fit)
	}
	return nil
}

func parse_place() (err error) {
	if opts.Place == "" {
		return nil
	}
	area, pos, found := strings.Cut(opts.Place, "@")
	if !found {
		return fmt.Errorf("Invalid --place specification: %s", opts.Place)
	}
	w, h, found := strings.Cut(area, "x")
	if !found {
		return fmt.Errorf("Invalid --place specification: %s", opts.Place)
	}
	l, t, found := strings.Cut(pos, "x")
	if !found {
		return fmt.Errorf("Invalid --place specification: %s", opts.Place)
	}
	place = &Place{}
	place.width, err = strconv.Atoi(w)
	if err != nil {
		return err
	}
	place.height, err = strconv.Atoi(h)
	if err != nil {
		return err
	}
	place.left, err = strconv.Atoi(l)
	if err != nil {
		return err
	}
	place.top, err = strconv.Atoi(t)
	if err != nil {
		return err
	}
	return nil
}

func print_error(format string, args ...any) {
	fmt.Fprintf(os.Stderr, format, args...)
	fmt.Fprintln(os.Stderr)
}

func main(cmd *cli.Command, o *Options, args []string) (rc int, err error) {
	opts = o
	if err = parse_place(); err != nil {
		return 1, err
	}
	if err = parse_fit(); err != nil {
		return 1, err
	}
	err = parse_z_index()
	if err != nil {
		return 1, err
	}
	err = parse_background()
	if err != nil {
		return 1, err
	}
	err = parse_mirror()
	if err != nil {
		return 1, err
	}
	if opts.UseWindowSize == "" {
		if tty.IsTerminal(os.Stdout.Fd()) {
			screen_size, err = tty.GetSize(int(os.Stdout.Fd()))
		} else {
			t, oerr := tty.OpenControllingTerm()
			if oerr != nil {
				return 1, fmt.Errorf("Failed to open controlling terminal with error: %w", oerr)
			}
			screen_size, err = t.GetSize()
		}
		if err != nil {
			return 1, fmt.Errorf("Failed to query terminal using TIOCGWINSZ with error: %w", err)
		}
	} else {
		parts := strings.SplitN(opts.UseWindowSize, ",", 4)
		if len(parts) != 4 {
			return 1, fmt.Errorf("Invalid size specification: %s", opts.UseWindowSize)
		}
		screen_size = &unix.Winsize{}
		var t uint64
		if t, err = strconv.ParseUint(parts[0], 10, 16); err != nil || t < 1 {
			return 1, fmt.Errorf("Invalid size specification: %s with error: %w", opts.UseWindowSize, err)
		}
		screen_size.Col = uint16(t)
		if t, err = strconv.ParseUint(parts[1], 10, 16); err != nil || t < 1 {
			return 1, fmt.Errorf("Invalid size specification: %s with error: %w", opts.UseWindowSize, err)
		}
		screen_size.Row = uint16(t)
		if t, err = strconv.ParseUint(parts[2], 10, 16); err != nil || t < 1 {
			return 1, fmt.Errorf("Invalid size specification: %s with error: %w", opts.UseWindowSize, err)
		}
		screen_size.Xpixel = uint16(t)
		if t, err = strconv.ParseUint(parts[3], 10, 16); err != nil || t < 1 {
			return 1, fmt.Errorf("Invalid size specification: %s with error: %w", opts.UseWindowSize, err)
		}
		screen_size.Ypixel = uint16(t)
		if screen_size.Xpixel < screen_size.Col {
			return 1, fmt.Errorf("Invalid size specification: %s with error: The pixel width is smaller than the number of columns", opts.UseWindowSize)
		}
		if screen_size.Ypixel < screen_size.Row {
			return 1, fmt.Errorf("Invalid size specification: %s with error: The pixel height is smaller than the number of rows", opts.UseWindowSize)
		}
	}

	if opts.PrintWindowSize {
		fmt.Printf("%dx%d", screen_size.Xpixel, screen_size.Ypixel)
		return 0, nil
	}
	if opts.Clear {
		cc := &graphics.GraphicsCommand{}
		cc.SetAction(graphics.GRT_action_delete).SetDelete(graphics.GRT_free_visible)
		if err = cc.WriteWithPayloadTo(os.Stdout, nil); err != nil {
			return 1, err
		}
	}
	switch {
	case opts.ClearAll:
		cc := &graphics.GraphicsCommand{}
		cc.SetAction(graphics.GRT_action_delete).SetDelete(graphics.GRT_free_by_range).SetLeftEdge(0).SetTopEdge(math.MaxUint32)
		if err = cc.WriteWithPayloadTo(os.Stdout, nil); err != nil {
			return 1, err
		}
	case opts.Clear:
		cc := &graphics.GraphicsCommand{}
		cc.SetAction(graphics.GRT_action_delete).SetDelete(graphics.GRT_free_visible)
		if err = cc.WriteWithPayloadTo(os.Stdout, nil); err != nil {
			return 1, err
		}
	}
	if screen_size.Xpixel == 0 || screen_size.Ypixel == 0 {
		return 1, fmt.Errorf("Terminal does not support reporting screen sizes in pixels, use a terminal such as kitty, WezTerm, Konsole, etc. that does.")
	}

	items, err := process_dirs(args...)
	if err != nil {
		return 1, err
	}
	if opts.Place != "" && len(items) > 1 {
		return 1, fmt.Errorf("The --place option can only be used with a single image, not %d", len(items))
	}
	files_channel = make(chan input_arg, len(items))
	for i, ia := range items {
		ia.index = i
		files_channel <- ia
	}
	num_of_items = len(items)
	output_channel = make(chan *image_data, 1)
	keep_going = &atomic.Bool{}
	keep_going.Store(true)
	if !opts.DetectSupport && num_of_items > 0 {
		num_workers := utils.Max(1, utils.Min(num_of_items, runtime.NumCPU()))
		for range num_workers {
			go run_worker()
		}
	}

	passthrough_mode := no_passthrough
	switch opts.Passthrough {
	case "tmux":
		passthrough_mode = tmux_passthrough
	case "detect":
		if tui.TmuxSocketAddress() != "" {
			passthrough_mode = tmux_passthrough
		}
	}

	if passthrough_mode == no_passthrough && (opts.TransferMode == "detect" || opts.DetectSupport) {
		memory, files, direct, err := DetectSupport(time.Duration(opts.DetectionTimeout * float64(time.Second)))
		if err != nil {
			return 1, err
		}
		if !direct {
			keep_going.Store(false)
			return 1, fmt.Errorf("This terminal does not support the graphics protocol use a terminal such as kitty, WezTerm or Konsole that does. If you are running inside a terminal multiplexer such as tmux or screen that might be interfering as well.")
		}
		if memory {
			transfer_by_memory = supported
		} else {
			transfer_by_memory = unsupported
		}
		if files {
			transfer_by_file = supported
		} else {
			transfer_by_file = unsupported
		}
	}
	if passthrough_mode != no_passthrough {
		// tmux doesn't allow responses from the terminal so we can't detect if memory or file based transferring is supported
		transfer_by_memory = unsupported
		transfer_by_file = unsupported
	}
	if opts.DetectSupport {
		if transfer_by_memory == supported {
			print_error("memory")
		} else if transfer_by_file == supported {
			print_error("files")
		} else {
			print_error("stream")
		}
		return 0, nil
	}
	use_unicode_placeholder := opts.UnicodePlaceholder
	if passthrough_mode != no_passthrough {
		use_unicode_placeholder = true
	}
	base_id := uint32(opts.ImageId)
	expecting_input_sequence_number := 0
	pending := make([]*image_data, 0, num_of_items)

	do_one := func(imgd *image_data) {
		expecting_input_sequence_number++
		if base_id != 0 {
			imgd.image_id = base_id
			base_id++
			if base_id == 0 {
				base_id++
			}
		}
		imgd.use_unicode_placeholder = use_unicode_placeholder
		imgd.passthrough_mode = passthrough_mode
		if imgd.err != nil {
			print_error("Failed to process \x1b[31m%s\x1b[39m: %s\r\n", imgd.source_name, imgd.err)
		} else {
			transmit_image(imgd, opts.NoTrailingNewline)
			if imgd.err != nil {
				print_error("Failed to transmit \x1b[31m%s\x1b[39m: %s\r\n", imgd.source_name, imgd.err)
			}
		}
	}

	for num_of_items > 0 {
		imgd := <-output_channel
		num_of_items--
		if imgd.input_sequence_number == expecting_input_sequence_number {
			do_one(imgd)
		} else {
			index, _ := slices.BinarySearchFunc(pending, imgd.input_sequence_number, func(x *image_data, n int) int {
				return x.input_sequence_number - n
			})
			pending = slices.Insert(pending, index, imgd)
		}
		for len(pending) > 0 && pending[0].input_sequence_number == expecting_input_sequence_number {
			do_one(pending[0])
			pending = pending[1:]
		}
	}
	for _, x := range pending {
		do_one(x)
	}
	keep_going.Store(false)
	if opts.Hold {
		fmt.Print("\r")
		if opts.Place != "" {
			fmt.Println()
		}
		tui.HoldTillEnter(false)
	}
	return 0, nil
}

func EntryPoint(parent *cli.Command) {
	create_cmd(parent, main)
}

```

## /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo/process_images.go

```
// License: GPLv3 Copyright: 2022, Kovid Goyal, <kovid at kovidgoyal.net>

package icat

import (
	"bytes"
	"fmt"
	"image"
	"io"
	"io/fs"
	"math"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"

	"github.com/kovidgoyal/imaging"
	"github.com/kovidgoyal/kitty/tools/tty"
	"github.com/kovidgoyal/kitty/tools/tui/graphics"
	"github.com/kovidgoyal/kitty/tools/utils"
	"github.com/kovidgoyal/kitty/tools/utils/images"
)

var _ = fmt.Print

type input_arg struct {
	arg         string
	value       string
	is_http_url bool
	index       int
}

func is_http_url(arg string) bool {
	return strings.HasPrefix(arg, "https://") || strings.HasPrefix(arg, "http://")
}

func process_dirs(args ...string) (results []input_arg, err error) {
	results = make([]input_arg, 0, 64)
	if opts.Stdin != "no" && (opts.Stdin == "yes" || !tty.IsTerminal(os.Stdin.Fd())) {
		results = append(results, input_arg{arg: "/dev/stdin"})
	}
	for _, arg := range args {
		if arg != "" {
			if is_http_url(arg) {
				results = append(results, input_arg{arg: arg, value: arg, is_http_url: true})
			} else {
				if strings.HasPrefix(arg, "file://") {
					u, err := url.Parse(arg)
					if err != nil {
						return nil, &fs.PathError{Op: "Parse", Path: arg, Err: err}
					}
					arg = u.Path
				}
				s, err := os.Stat(arg)
				if err != nil {
					return nil, &fs.PathError{Op: "Stat", Path: arg, Err: err}
				}
				if s.IsDir() {
					if err = filepath.WalkDir(arg, func(path string, d fs.DirEntry, walk_err error) error {
						if walk_err != nil {
							if d == nil {
								err = &fs.PathError{Op: "Stat", Path: arg, Err: walk_err}
							}
							return walk_err
						}
						if !d.IsDir() {
							mt := utils.GuessMimeType(path)
							if strings.HasPrefix(mt, "image/") {
								results = append(results, input_arg{arg: arg, value: path})
							}
						}
						return nil
					}); err != nil {
						return nil, err
					}
				} else {
					results = append(results, input_arg{arg: arg, value: arg})
				}
			}
		}
	}
	return results, nil
}

type opened_input struct {
	file  io.Reader
	bytes []byte
	path  string
}

type image_frame struct {
	filename                 string
	in_memory_bytes          []byte
	width, height, left, top int
	transmission_format      graphics.GRT_f
	compose_onto             int
	replace                  bool
	number                   int
	delay_ms                 int
}

type image_data struct {
	canvas_width, canvas_height       int
	format_uppercase                  string
	available_width, available_height int
	needs_scaling                     bool
	frames                            []*image_frame
	image_number                      uint32
	image_id                          uint32
	cell_x_offset                     int
	move_x_by                         int
	move_to                           struct{ x, y int }
	width_cells, height_cells         int
	use_unicode_placeholder           bool
	passthrough_mode                  passthrough_type
	input_sequence_number             int

	// for error reporting
	err         error
	source_name string
}

const inf = math.MaxInt

func set_basic_metadata(imgd *image_data) {
	if imgd.frames == nil {
		imgd.frames = make([]*image_frame, 0, 32)
	}
	if place != nil {
		imgd.available_width = place.width * int(screen_size.Xpixel) / int(screen_size.Col)
		imgd.available_height = place.height * int(screen_size.Ypixel) / int(screen_size.Row)
	} else {
		switch fit_mode {
		case fit_none:
			imgd.available_width, imgd.available_height = inf, inf
		case fit_both:
			imgd.available_width = int(screen_size.Xpixel)
			imgd.available_height = int(screen_size.Ypixel)
		case fit_width:
			imgd.available_width = int(screen_size.Xpixel)
			imgd.available_height = inf
		case fit_height:
			imgd.available_width = inf
			imgd.available_height = int(screen_size.Ypixel)
		}
	}
	imgd.needs_scaling = imgd.canvas_width > imgd.available_width || imgd.canvas_height > imgd.available_height || opts.ScaleUp
}

func report_error(source_name, msg string, err error) {
	imgd := image_data{source_name: source_name, err: fmt.Errorf("%s: %w", msg, err)}
	send_output(&imgd)
}

func make_output_from_input(imgd *image_data, f *opened_input) {
	frame := image_frame{}
	imgd.frames = append(imgd.frames, &frame)
	frame.width = imgd.canvas_width
	frame.height = imgd.canvas_height
	if imgd.format_uppercase != "PNG" {
		panic(fmt.Sprintf("Unknown transmission format: %s", imgd.format_uppercase))
	}
	frame.transmission_format = graphics.GRT_format_png
	if f.bytes != nil {
		frame.in_memory_bytes = f.bytes
	} else if f.path != "" {
		frame.filename = f.path
	} else {
		var err error
		if frame.in_memory_bytes, err = io.ReadAll(f.file); err != nil {
			panic(err)
		}
	}
}

func scale_up(width, height, maxWidth, maxHeight int) (newWidth, newHeight int) {
	if width == 0 || height == 0 {
		return 0, 0
	}
	// Calculate the ratio to scale the width and the ratio to scale the height.
	// We use floating-point division for precision.
	widthRatio := float64(maxWidth) / float64(width)
	heightRatio := float64(maxHeight) / float64(height)

	// To preserve the aspect ratio and fit within the limits, we must use the
	// smaller of the two scaling ratios.
	var ratio float64
	if widthRatio < heightRatio {
		ratio = widthRatio
	} else {
		ratio = heightRatio
	}

	// Calculate the new dimensions and convert them back to uints.
	newWidth = int(float64(width) * ratio)
	newHeight = int(float64(height) * ratio)

	return newWidth, newHeight
}

func scale_image(imgd *image_data) bool {
	if imgd.needs_scaling {
		width, height := imgd.canvas_width, imgd.canvas_height
		if opts.ScaleUp && (imgd.canvas_width < imgd.available_width || imgd.canvas_height < imgd.available_height) && (imgd.available_height != inf || imgd.available_width != inf) {
			imgd.canvas_width, imgd.canvas_height = scale_up(imgd.canvas_width, imgd.canvas_height, imgd.available_width, imgd.available_height)
		}
		neww, newh := images.FitImage(imgd.canvas_width, imgd.canvas_height, imgd.available_width, imgd.available_height)
		imgd.needs_scaling = false
		x := float64(neww) / float64(width)
		y := float64(newh) / float64(height)
		imgd.canvas_width = int(x * float64(width))
		imgd.canvas_height = int(y * float64(height))
		return true
	}
	return false
}

func add_frame(imgd *image_data, img image.Image, left, top int) *image_frame {
	const shm_template = "kitty-icat-*"
	num_channels := 4
	var pix []byte
	if imaging.IsOpaque(img) {
		num_channels, pix = 3, imaging.AsRGBData8(img)
	} else {
		pix = imaging.AsRGBAData8(img)
	}
	b := img.Bounds()
	f := image_frame{width: b.Dx(), height: b.Dy(), number: len(imgd.frames) + 1, left: left, top: top}
	f.transmission_format = utils.IfElse(num_channels == 3, graphics.GRT_format_rgb, graphics.GRT_format_rgba)
	f.in_memory_bytes = pix
	imgd.frames = append(imgd.frames, &f)
	return &f
}

func process_arg(arg input_arg) {
	var f opened_input
	if arg.is_http_url {
		resp, err := http.Get(arg.value)
		if err != nil {
			report_error(arg.value, "Could not get", err)
			return
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			report_error(arg.value, "Could not get", fmt.Errorf("bad status: %v", resp.Status))
			return
		}
		dest := bytes.Buffer{}
		dest.Grow(64 * 1024)
		_, err = io.Copy(&dest, resp.Body)
		if err != nil {
			report_error(arg.value, "Could not download", err)
			return
		}
		f.bytes = dest.Bytes()
		f.file = bytes.NewReader(f.bytes)
	} else if arg.value == "" {
		stdin, err := io.ReadAll(os.Stdin)
		if err != nil {
			report_error("<stdin>", "Could not read from", err)
			return
		}
		f.bytes = stdin
		f.file = bytes.NewReader(f.bytes)
	} else {
		q, err := os.Open(arg.value)
		if err != nil {
			report_error(arg.value, "Could not open", err)
			return
		}
		f.file = q
		f.path = q.Name()
		defer q.Close()
	}

	var img *images.ImageData
	var dopts []imaging.DecodeOption
	needs_conversion := false
	if flip {
		dopts = append(dopts, imaging.Transform(imaging.FlipVTransform))
		needs_conversion = true
	}
	if flop {
		dopts = append(dopts, imaging.Transform(imaging.FlipHTransform))
		needs_conversion = true
	}
	if remove_alpha != nil {
		dopts = append(dopts, imaging.Background(*remove_alpha))
		needs_conversion = true
	}
	switch opts.Engine {
	case "native", "builtin":
		dopts = append(dopts, imaging.Backends(imaging.GO_IMAGE))
	case "magick":
		dopts = append(dopts, imaging.Backends(imaging.MAGICK_IMAGE))
	}
	imgd := image_data{source_name: arg.value, input_sequence_number: arg.index}
	dopts = append(dopts, imaging.ResizeCallback(func(w, h int) (int, int) {
		imgd.canvas_width, imgd.canvas_height = w, h
		set_basic_metadata(&imgd)
		if scale_image(&imgd) {
			needs_conversion = true
			w, h = imgd.canvas_width, imgd.canvas_height
		}
		return w, h
	}))
	var err error
	if f.path != "" {
		img, err = images.OpenImageFromPath(f.path, dopts...)
	} else {
		img, f.file, err = images.OpenImageFromReader(f.file, dopts...)
	}
	if err != nil {
		report_error(arg.value, "Could not render image to RGB", err)
		return
	}
	if !keep_going.Load() {
		return
	}
	imgd.format_uppercase = img.Format_uppercase
	imgd.canvas_width, imgd.canvas_height = img.Width, img.Height
	if !needs_conversion && imgd.format_uppercase == "PNG" && len(img.Frames) == 1 {
		make_output_from_input(&imgd, &f)
	} else {
		for _, f := range img.Frames {
			frame := add_frame(&imgd, f.Img, f.Left, f.Top)
			frame.number, frame.compose_onto = int(f.Number), int(f.Compose_onto)
			frame.replace = f.Replace
			frame.delay_ms = int(f.Delay_ms)
		}
	}
	if !keep_going.Load() {
		return
	}
	send_output(&imgd)
}

func run_worker() {
	for {
		select {
		case arg := <-files_channel:
			if !keep_going.Load() {
				return
			}
			process_arg(arg)
		default:
			return
		}
	}
}

```

## /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo/transmit.go

```
// License: GPLv3 Copyright: 2022, Kovid Goyal, <kovid at kovidgoyal.net>

package icat

import (
	"bytes"
	"crypto/rand"
	"encoding/binary"
	"fmt"
	"github.com/kovidgoyal/kitty"
	"io"
	"math"
	not_rand "math/rand/v2"
	"os"
	"path/filepath"
	"strings"

	"github.com/kovidgoyal/go-shm"
	"github.com/kovidgoyal/kitty/tools/tui"
	"github.com/kovidgoyal/kitty/tools/tui/graphics"
	"github.com/kovidgoyal/kitty/tools/tui/loop"
	"github.com/kovidgoyal/kitty/tools/utils"
	"github.com/kovidgoyal/kitty/tools/utils/images"
)

var _ = fmt.Print

type passthrough_type int

const (
	no_passthrough passthrough_type = iota
	tmux_passthrough
)

func new_graphics_command(imgd *image_data) *graphics.GraphicsCommand {
	gc := graphics.GraphicsCommand{}
	switch imgd.passthrough_mode {
	case tmux_passthrough:
		gc.WrapPrefix = "\033Ptmux;"
		gc.WrapSuffix = "\033\\"
		gc.EncodeSerializedDataFunc = func(x string) string { return strings.ReplaceAll(x, "\033", "\033\033") }
	}
	return &gc
}

func gc_for_image(imgd *image_data, frame_num int, frame *image_frame) *graphics.GraphicsCommand {
	gc := new_graphics_command(imgd)
	gc.SetDataWidth(uint64(frame.width)).SetDataHeight(uint64(frame.height))
	gc.SetQuiet(graphics.GRT_quiet_silent)
	gc.SetFormat(frame.transmission_format)
	if imgd.image_number != 0 {
		gc.SetImageNumber(imgd.image_number)
	}
	if imgd.image_id != 0 {
		gc.SetImageId(imgd.image_id)
	}
	if frame_num == 0 {
		gc.SetAction(graphics.GRT_action_transmit_and_display)
		if imgd.use_unicode_placeholder {
			gc.SetUnicodePlaceholder(graphics.GRT_create_unicode_placeholder)
			gc.SetColumns(uint64(imgd.width_cells))
			gc.SetRows(uint64(imgd.height_cells))
		}
		if imgd.cell_x_offset > 0 {
			gc.SetXOffset(uint64(imgd.cell_x_offset))
		}
		if z_index != 0 {
			gc.SetZIndex(z_index)
		}
		if place != nil {
			gc.SetCursorMovement(graphics.GRT_cursor_static)
		}
	} else {
		gc.SetAction(graphics.GRT_action_frame)
		gc.SetGap(int32(frame.delay_ms))
		gc.SetCompositionMode(utils.IfElse(frame.replace, graphics.Overwrite, graphics.AlphaBlend))
		if frame.compose_onto > 0 {
			gc.SetOverlaidFrame(uint64(frame.compose_onto))
		}
		gc.SetLeftEdge(uint64(frame.left)).SetTopEdge(uint64(frame.top))
	}
	return gc
}

func transmit_shm(imgd *image_data, frame_num int, frame *image_frame) (err error) {
	var mmap shm.MMap
	var data_size int64
	if frame.in_memory_bytes == nil {
		f, err := os.Open(frame.filename)
		if err != nil {
			return fmt.Errorf("Failed to open image data output file: %s with error: %w", frame.filename, err)
		}
		defer f.Close()
		if data_size, err = f.Seek(0, io.SeekEnd); err != nil {
			return fmt.Errorf("Failed to seek in image data output file: %s with error: %w", frame.filename, err)
		}
		if _, err = f.Seek(0, io.SeekStart); err != nil {
			return fmt.Errorf("Failed to seek in image data output file: %s with error: %w", frame.filename, err)
		}
		if mmap, err = shm.CreateTemp("icat-*", uint64(data_size)); err != nil {
			return fmt.Errorf("Failed to create a SHM file for transmission: %w", err)
		}
		if _, err = io.ReadFull(f, mmap.Slice()); err != nil {
			mmap.Close()
			mmap.Unlink()
			return fmt.Errorf("Failed to read data from image output data file: %w", err)
		}
	} else {
		data_size = int64(len(frame.in_memory_bytes))
		if mmap, err = shm.CreateTemp("icat-*", uint64(data_size)); err != nil {
			return fmt.Errorf("Failed to create a SHM file for transmission: %w", err)
		}
		copy(mmap.Slice(), frame.in_memory_bytes)
	}
	defer mmap.Close() // terminal is responsible for unlink
	gc := gc_for_image(imgd, frame_num, frame)
	gc.SetTransmission(graphics.GRT_transmission_sharedmem)
	gc.SetDataSize(uint64(data_size))
	err = gc.WriteWithPayloadTo(os.Stdout, utils.UnsafeStringToBytes(mmap.Name()))
	return
}

func transmit_file(imgd *image_data, frame_num int, frame *image_frame) (err error) {
	is_temp := false
	fname := ""
	var data_size int
	if frame.in_memory_bytes == nil {
		fname, err = filepath.Abs(frame.filename)
		if err != nil {
			return fmt.Errorf("Failed to convert image data output file: %s to absolute path with error: %w", frame.filename, err)
		}
		frame.filename = "" // so it isn't deleted in cleanup
	} else {
		is_temp = true
		f, err := images.CreateTempInRAM()
		if err != nil {
			return fmt.Errorf("Failed to create a temp file for image data transmission: %w", err)
		}
		data_size = len(frame.in_memory_bytes)
		_, err = bytes.NewBuffer(frame.in_memory_bytes).WriteTo(f)
		f.Close()
		if err != nil {
			os.Remove(f.Name())
			return fmt.Errorf("Failed to write image data to temp file for transmission: %w", err)
		}
		fname = f.Name()
	}
	gc := gc_for_image(imgd, frame_num, frame)
	gc.SetTransmission(utils.IfElse(is_temp, graphics.GRT_transmission_tempfile, graphics.GRT_transmission_file))
	if data_size > 0 {
		gc.SetDataSize(uint64(data_size))
	}
	return gc.WriteWithPayloadTo(os.Stdout, utils.UnsafeStringToBytes(fname))
}

func transmit_stream(imgd *image_data, frame_num int, frame *image_frame) (err error) {
	data := frame.in_memory_bytes
	if data == nil {
		data, err = os.ReadFile(frame.filename)
		if err != nil {
			return fmt.Errorf("Failed to read image data output file: %s with error: %w", frame.filename, err)
		}
	}
	gc := gc_for_image(imgd, frame_num, frame)
	return gc.WriteWithPayloadTo(os.Stdout, data)
}

func calculate_in_cell_x_offset(width, cell_width int) int {
	extra_pixels := width % cell_width
	if extra_pixels == 0 {
		return 0
	}
	switch opts.Align {
	case "left":
		return 0
	case "right":
		return cell_width - extra_pixels
	default:
		return (cell_width - extra_pixels) / 2
	}
}

func place_cursor(imgd *image_data) {
	cw := max(int(screen_size.Xpixel)/int(screen_size.Col), 1)
	ch := max(int(screen_size.Ypixel)/int(screen_size.Row), 1)
	imgd.cell_x_offset = calculate_in_cell_x_offset(imgd.canvas_width, cw)
	imgd.width_cells = int(math.Ceil(float64(imgd.canvas_width) / float64(cw)))
	imgd.height_cells = int(math.Ceil(float64(imgd.canvas_height) / float64(ch)))
	if place == nil {
		switch opts.Align {
		case "center":
			imgd.move_x_by = (int(screen_size.Col) - imgd.width_cells) / 2
		case "right":
			imgd.move_x_by = (int(screen_size.Col) - imgd.width_cells)
		}
	} else {
		imgd.move_to.x = place.left + 1
		imgd.move_to.y = place.top + 1
		switch opts.Align {
		case "center":
			imgd.move_to.x += (place.width - imgd.width_cells) / 2
		case "right":
			imgd.move_to.x += (place.width - imgd.width_cells)
		}
	}
}

func next_random() (ans uint32) {
	for ans == 0 {
		b := make([]byte, 4)
		_, err := rand.Read(b)
		if err == nil {
			ans = binary.LittleEndian.Uint32(b[:])
		} else {
			ans = not_rand.Uint32()
		}
	}
	return ans
}

func write_unicode_placeholder(imgd *image_data) {
	prefix := ""
	foreground := fmt.Sprintf("\033[38:2:%d:%d:%dm", (imgd.image_id>>16)&255, (imgd.image_id>>8)&255, imgd.image_id&255)
	os.Stdout.WriteString(foreground)
	restore := "\033[39m"
	if imgd.move_to.y > 0 {
		os.Stdout.WriteString(loop.SAVE_CURSOR)
		restore += loop.RESTORE_CURSOR
	} else if imgd.move_x_by > 0 {
		prefix = strings.Repeat(" ", imgd.move_x_by)
	}
	defer func() { os.Stdout.WriteString(restore) }()
	if imgd.move_to.y > 0 {
		fmt.Printf(loop.MoveCursorToTemplate, imgd.move_to.y, 0)
	}
	id_char := string(images.NumberToDiacritic[(imgd.image_id>>24)&255])
	for r := 0; r < imgd.height_cells; r++ {
		if imgd.move_to.x > 0 {
			fmt.Printf("\x1b[%dC", imgd.move_to.x-1)
		} else {
			os.Stdout.WriteString(prefix)
		}
		for c := 0; c < imgd.width_cells; c++ {
			os.Stdout.WriteString(string(kitty.ImagePlaceholderChar) + string(images.NumberToDiacritic[r]) + string(images.NumberToDiacritic[c]) + id_char)
		}
		if r < imgd.height_cells-1 {
			os.Stdout.WriteString("\n\r")
		}
	}
}

var seen_image_ids *utils.Set[uint32]

func transmit_image(imgd *image_data, no_trailing_newline bool) {
	if seen_image_ids == nil {
		seen_image_ids = utils.NewSet[uint32](32)
	}
	var f func(*image_data, int, *image_frame) error
	if opts.TransferMode != "detect" {
		switch opts.TransferMode {
		case "file":
			f = transmit_file
		case "memory":
			f = transmit_shm
		case "stream":
			f = transmit_stream
		}
	}
	if f == nil && transfer_by_memory == supported && imgd.frames[0].in_memory_bytes != nil {
		f = transmit_shm
	}
	if f == nil && transfer_by_file == supported {
		f = transmit_file
	}
	if f == nil {
		f = transmit_stream
	}
	if imgd.image_id == 0 {
		if imgd.use_unicode_placeholder {
			for imgd.image_id&0xFF000000 == 0 || imgd.image_id&0x00FFFF00 == 0 || seen_image_ids.Has(imgd.image_id) {
				// Generate a 32-bit image id using rejection sampling such that the most
				// significant byte and the two bytes in the middle are non-zero to avoid
				// collisions with applications that cannot represent non-zero most
				// significant bytes (which is represented by the third combining character)
				// or two non-zero bytes in the middle (which requires 24-bit color mode).
				imgd.image_id = next_random()
			}
			seen_image_ids.Add(imgd.image_id)
		} else {
			if len(imgd.frames) > 1 {
				for imgd.image_number == 0 {
					imgd.image_number = next_random()
				}
			}
		}
	}
	place_cursor(imgd)
	if imgd.use_unicode_placeholder && utils.Max(imgd.width_cells, imgd.height_cells) >= len(images.NumberToDiacritic) {
		imgd.err = fmt.Errorf("Image too large to be displayed using Unicode placeholders. Maximum size is %dx%d cells", len(images.NumberToDiacritic), len(images.NumberToDiacritic))
		return
	}
	switch imgd.passthrough_mode {
	case tmux_passthrough:
		imgd.err = tui.TmuxAllowPassthrough()
		if imgd.err != nil {
			return
		}
	}
	fmt.Print("\r")
	if !imgd.use_unicode_placeholder {
		if imgd.move_x_by > 0 {
			fmt.Printf("\x1b[%dC", imgd.move_x_by)
		}
		if imgd.move_to.x > 0 {
			fmt.Printf(loop.MoveCursorToTemplate, imgd.move_to.y, imgd.move_to.x)
		}
	}
	frame_control_cmd := new_graphics_command(imgd)
	frame_control_cmd.SetAction(graphics.GRT_action_animate)
	if imgd.image_id != 0 {
		frame_control_cmd.SetImageId(imgd.image_id)
	} else {
		frame_control_cmd.SetImageNumber(imgd.image_number)
	}
	is_animated := len(imgd.frames) > 1

	for frame_num, frame := range imgd.frames {
		err := f(imgd, frame_num, frame)
		if err != nil {
			imgd.err = err
			return
		}
		if is_animated {
			switch frame_num {
			case 0:
				// set gap for the first frame and number of loops for the animation
				c := frame_control_cmd
				c.SetTargetFrame(uint64(frame.number))
				c.SetGap(int32(frame.delay_ms))
				switch {
				case opts.Loop < 0:
					c.SetNumberOfLoops(1)
				case opts.Loop > 0:
					c.SetNumberOfLoops(uint64(opts.Loop) + 1)
				}
				if imgd.err = c.WriteWithPayloadTo(os.Stdout, nil); imgd.err != nil {
					return
				}
			case 1:
				c := frame_control_cmd
				c.SetAnimationControl(2) // set animation to loading mode
				if imgd.err = c.WriteWithPayloadTo(os.Stdout, nil); imgd.err != nil {
					return
				}
			}
		}
	}
	if imgd.use_unicode_placeholder {
		write_unicode_placeholder(imgd)
	}
	if is_animated {
		c := frame_control_cmd
		c.SetAnimationControl(3) // set animation to normal mode
		if imgd.err = c.WriteWithPayloadTo(os.Stdout, nil); imgd.err != nil {
			return
		}
	}
	if imgd.move_to.x == 0 && !no_trailing_newline {
		fmt.Println() // ensure cursor is on new line
	}
}

```

## /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo/detect.go

```
// License: GPLv3 Copyright: 2023, Kovid Goyal, <kovid at kovidgoyal.net>

package icat

import (
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/kovidgoyal/go-shm"
	"github.com/kovidgoyal/kitty/tools/tui/graphics"
	"github.com/kovidgoyal/kitty/tools/tui/loop"
	"github.com/kovidgoyal/kitty/tools/utils"
	"github.com/kovidgoyal/kitty/tools/utils/images"
)

var _ = fmt.Print

func DetectSupport(timeout time.Duration) (memory, files, direct bool, err error) {
	temp_files_to_delete := make([]string, 0, 8)
	shm_files_to_delete := make([]shm.MMap, 0, 8)
	var direct_query_id, file_query_id, memory_query_id uint32
	lp, e := loop.New(loop.NoAlternateScreen, loop.NoRestoreColors, loop.NoMouseTracking, loop.NoInBandResizeNotifications)
	if e != nil {
		err = e
		return
	}
	print_error := func(format string, args ...any) {
		lp.Println(fmt.Sprintf(format, args...))
	}

	defer func() {
		if len(temp_files_to_delete) > 0 && transfer_by_file != supported {
			for _, name := range temp_files_to_delete {
				os.Remove(name)
			}
		}
		if len(shm_files_to_delete) > 0 && transfer_by_memory != supported {
			for _, name := range shm_files_to_delete {
				_ = name.Unlink()
			}
		}
	}()

	lp.OnInitialize = func() (string, error) {
		var iid uint32
		_, _ = lp.AddTimer(timeout, false, func(loop.IdType) error {
			return fmt.Errorf("Timed out waiting for a response from the terminal: %w", os.ErrDeadlineExceeded)
		})

		g := func(t graphics.GRT_t, payload string) uint32 {
			iid += 1
			g1 := &graphics.GraphicsCommand{}
			g1.SetTransmission(t).SetAction(graphics.GRT_action_query).SetImageId(iid).SetDataWidth(1).SetDataHeight(1).SetFormat(
				graphics.GRT_format_rgb).SetDataSize(uint64(len(payload)))
			_ = g1.WriteWithPayloadToLoop(lp, utils.UnsafeStringToBytes(payload))
			return iid
		}

		direct_query_id = g(graphics.GRT_transmission_direct, "123")
		tf, err := images.CreateTempInRAM()
		if err == nil {
			file_query_id = g(graphics.GRT_transmission_tempfile, tf.Name())
			temp_files_to_delete = append(temp_files_to_delete, tf.Name())
			if _, err = tf.Write([]byte{1, 2, 3}); err != nil {
				print_error("Failed to write to temporary file for data transfer, file based transfer is disabled. Error: %v", err)
			}
			tf.Close()
		} else {
			print_error("Failed to create temporary file for data transfer, file based transfer is disabled. Error: %v", err)
		}
		sf, err := shm.CreateTemp("icat-", 3)
		if err == nil {
			memory_query_id = g(graphics.GRT_transmission_sharedmem, sf.Name())
			shm_files_to_delete = append(shm_files_to_delete, sf)
			copy(sf.Slice(), []byte{1, 2, 3})
			sf.Close()
		} else {
			var ens *shm.ErrNotSupported
			if !errors.As(err, &ens) {
				print_error("Failed to create SHM for data transfer, memory based transfer is disabled. Error: %v", err)
			}
		}
		lp.QueueWriteString("\x1b[c")

		return "", nil
	}

	lp.OnEscapeCode = func(etype loop.EscapeCodeType, payload []byte) (err error) {
		switch etype {
		case loop.CSI:
			if len(payload) > 3 && payload[0] == '?' && payload[len(payload)-1] == 'c' {
				lp.Quit(0)
				return nil
			}
		case loop.APC:
			g := graphics.GraphicsCommandFromAPC(payload)
			if g != nil {
				if g.ResponseMessage() == "OK" {
					switch g.ImageId() {
					case direct_query_id:
						direct = true
					case file_query_id:
						files = true
					case memory_query_id:
						memory = true
					}
				}
				return
			}
		}
		return
	}

	lp.OnKeyEvent = func(event *loop.KeyEvent) error {
		if event.MatchesPressOrRepeat("ctrl+c") {
			event.Handled = true
			print_error("Waiting for response from terminal, aborting now could lead to corruption")
		}
		if event.MatchesPressOrRepeat("ctrl+z") {
			event.Handled = true
		}
		return nil
	}

	err = lp.Run()
	if err != nil {
		return
	}
	ds := lp.DeathSignalName()
	if ds != "" {
		fmt.Println("Killed by signal: ", ds)
		lp.KillIfSignalled()
		return
	}

	return
}

```

## /home/daniel/tron/programas/TR/docs/DISENO-INTERFAZ/icat repo/scaling_test.go

```
package icat

import (
	"fmt"
	"image"
	"testing"
)

var _ = fmt.Print

func TestScaling(t *testing.T) {
	for _, tc := range []struct {
		w, h, pw, ph, ew, eh int
	}{
		{1000, 50, 800, 600, 800, 40},
		{1000, 50, 800000, 600, 12000, 600},
		{100, 50, 800, 600, 800, 400},
		{1920, 1080, 800, 600, 800, 450},
		{300, 900, 800, 600, 200, 600},
		{400, 300, 800, 600, 800, 600},
	} {
		aw, ah := scale_up(tc.w, tc.h, tc.pw, tc.ph)
		actual := image.Pt(aw, ah)
		expected := image.Pt(tc.ew, tc.eh)
		if actual != expected {
			t.Fatalf("want: %v got: %v", expected, actual)
		}
	}
}

```

