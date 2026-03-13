## Contents

[](https://github.com/AnonymouX47/term-image#contents)

- [Installation](https://github.com/AnonymouX47/term-image#installation)
- [Features](https://github.com/AnonymouX47/term-image#features)
- [Demo](https://github.com/AnonymouX47/term-image#demo)
- [Quick Start](https://github.com/AnonymouX47/term-image#library-quick-start)
- [Usage](https://github.com/AnonymouX47/term-image#usage)
- [Contribution](https://github.com/AnonymouX47/term-image#contribution)
- [Planned Features](https://github.com/AnonymouX47/term-image#planned-features)
- [Known Issues](https://github.com/AnonymouX47/term-image#known-issues)
- [FAQs](https://github.com/AnonymouX47/term-image#faqs)
- [Credits](https://github.com/AnonymouX47/term-image#credits)
- [Sponsor This Project](https://github.com/AnonymouX47/term-image#sponsor-this-project)

> ### ⚠️ NOTICE!!! ⚠️
> 
> [](https://github.com/AnonymouX47/term-image#%EF%B8%8F-notice-%EF%B8%8F)
> 
> The image viewer (CLI and TUI) has been moved to [termvisage](https://github.com/AnonymouX47/termvisage).

## Installation

[](https://github.com/AnonymouX47/term-image#installation)



[Term-Image 0.7.2 documentation](https://term-image.readthedocs.io/en/stable/)



## Contents

- [Getting Started](https://term-image.readthedocs.io/en/stable/start/index.html)
  - [Installation](https://term-image.readthedocs.io/en/stable/start/installation.html)
  - [Tutorial](https://term-image.readthedocs.io/en/stable/start/tutorial.html)
- [User Guide](https://term-image.readthedocs.io/en/stable/guide/index.html)
  - [Concepts](https://term-image.readthedocs.io/en/stable/guide/concepts.html)
  - [Render Formatting](https://term-image.readthedocs.io/en/stable/guide/formatting.html)
- [API Reference](https://term-image.readthedocs.io/en/stable/api/index.html)
  - [Top-Level Definitions](https://term-image.readthedocs.io/en/stable/api/toplevel.html)
  - [`image` Module](https://term-image.readthedocs.io/en/stable/api/image.html)
  - [`widget` Module](https://term-image.readthedocs.io/en/stable/api/widget.html)
  - [`exceptions` Module](https://term-image.readthedocs.io/en/stable/api/exceptions.html)
  - [`utils` Module](https://term-image.readthedocs.io/en/stable/api/utils.html)
- [Planned Features](https://term-image.readthedocs.io/en/stable/planned.html)
- [Known Issues](https://term-image.readthedocs.io/en/stable/issues.html)
- [FAQs](https://term-image.readthedocs.io/en/stable/faqs.html)
- [Glossary](https://term-image.readthedocs.io/en/stable/glossary.html)

## Indices and Tables

- [Index](https://term-image.readthedocs.io/en/stable/genindex.html)

- [Module Index](https://term-image.readthedocs.io/en/stable/py-modindex.html)

[

](https://term-image.readthedocs.io/en/stable/start/index.html)



# Tutorial

This is a basic introduction to using the library. Please refer to the [API Reference](https://term-image.readthedocs.io/en/stable/api/index.html) for detailed description of the features and functionality provided by the library.

For this tutorial we’ll be using the image below:

![../_images/python.png](https://term-image.readthedocs.io/en/stable/_images/python.png)

The image has a resolution of **288x288 pixels**.

Note

All the samples in this tutorial occurred in a terminal window of **255 columns by 70 lines**.

## Creating an Instance

Image instances can be created using the convenience functions [`AutoImage()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.AutoImage "term_image.image.AutoImage"), [`from_file()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_file "term_image.image.from_file") and [`from_url()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_url "term_image.image.from_url"), which automatically detect the best style supported by the terminal emulator.

Instances can also be created using the [Image Classes](https://term-image.readthedocs.io/en/stable/api/image.html#image-classes) directly via their respective constructors or [`from_file()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.from_file "term_image.image.BaseImage.from_file") and [`from_url()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.from_url "term_image.image.BaseImage.from_url") methods.

1. Initialize with a file path:
   
   from term_image.image import from_file
   
   image = from_file("path/to/python.png")

2. Initialize with a URL:
   
   from term_image.image import from_url
   
   image = from_url("https://raw.githubusercontent.com/AnonymouX47/term-image/main/docs/source/resources/tutorial/python.png")

3. Initialize with a PIL (Pillow) image instance:
   
   from PIL import Image
   from term_image.image import AutoImage
   
   img = Image.open("path/to/python.png")
   image = AutoImage(img)

## Rendering an Image

Rendering an image is the process of converting it (per-frame for [animated](https://term-image.readthedocs.io/en/stable/glossary.html#term-animated) images) into text (a string) which reproduces a representation or approximation of the image when written to the terminal.

Hint

To display the rendered image in the following steps, pass the string as an argument to [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)").

There are two ways to render an image:

### Unformatted Rendering

This is done using:

str(image)

The image is rendered without *padding*/*alignment* and with transparency enabled.

The output (using [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)")) should look like:

![../_images/str.png](https://term-image.readthedocs.io/en/stable/_images/str.png)

### Formatted Rendering

Note

To see the effect of [alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-alignment) in the steps below, set the image size **smaller** than **your** terminal size, with e.g:

image.height = 50

This sets the image height to `50` lines (which is less than `70`, the height of the terminal window used to prepare this tutorial) and the width proportionally.

We’ll see more about this later.

Below are examples of formatted rendering:

format(image, "|200.^70#ffffff")

Renders the image with:

- **center** [horizontal alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment)

- a [padding width](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-width) of **200** columns

- **top** [vertical alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment)

- a [padding height](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-height) of **70** lines

- **white** (`#ffffff`) background underlay

Note

You might have to reduce the padding width (200) and/or height (70) to something that’ll fit into your terminal window, or increase the size of the terminlal window

The output (using [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)")) should look like:

![../_images/white_bg.png](https://term-image.readthedocs.io/en/stable/_images/white_bg.png)

f"{image:>._#.5}"

Renders the image with:

- **right** [horizontal alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment)

- **default** [padding width](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-width) (the current [terminal width](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-width))

- **bottom** [vertical alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment)

- **default** [padding height](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-height) (the current [terminal height](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-height) minus two (`2`))

- transparent background with **0.5** [alpha threshold](https://term-image.readthedocs.io/en/stable/glossary.html#term-alpha-threshold)

The output (using [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)")) should look like:

![../_images/alpha_0_5.png](https://term-image.readthedocs.io/en/stable/_images/alpha_0_5.png)

"{:1.1#}".format(image)

Renders the image with:

- **center** [horizontal alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment) (default)

- **no** horizontal [padding](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding), since `1` is less than or equal to the image width

- **middle** [vertical alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment) (default)

- **no** vertical [padding](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding), since `1` is less than or equal to the image height

- transparency is **disabled** (alpha channel is ignored)

The output (using [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)")) should look like:

![../_images/no_alpha_no_align.png](https://term-image.readthedocs.io/en/stable/_images/no_alpha_no_align.png)

See also

[Render Formatting](https://term-image.readthedocs.io/en/stable/guide/formatting.html) and [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)

## Drawing/Displaying an Image

There are two basic ways to draw an image to the terminal screen:

1. Using the [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw") method:
   
   image.draw()
   
   **NOTE:** [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw") has various parameters for [Render Formatting](https://term-image.readthedocs.io/en/stable/guide/formatting.html).

2. Using [`print()`](https://docs.python.org/3/library/functions.html#print "(in Python v3.12)") with an image render output (i.e printing the rendered string):
   
   print(image)  # Uses str()
   
   # OR
   
   print(f"{image:>200.^70#ffffff}")  # Uses format()

Note

- For [animated](https://term-image.readthedocs.io/en/stable/glossary.html#term-animated) images, only the former animates the output, the latter only draws the **current** frame (see [`seek()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.seek "term_image.image.BaseImage.seek") and [`tell()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.tell "term_image.image.BaseImage.tell")).

- Also, the former performs size validation to see if the image will fit into the terminal, while the latter doesn’t.

Important

All the examples **above** use [dynamic](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-size) and [automatic](https://term-image.readthedocs.io/en/stable/glossary.html#term-automatic-size) sizing.

## Image Size

The size of an image determines the dimension of its render output.

The image size can be retrieved via the [`size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.size "term_image.image.BaseImage.size"), [`width`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.width "term_image.image.BaseImage.width") and [`height`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.height "term_image.image.BaseImage.height") properties.

The size of an image can be in either of two states:

1. Fixed
   
   In this state,
   
   - the `size` property evaluates to a 2-tuple of integers, while the `width` and `height` properties evaluate to integers,
   
   - the image is rendered with the set size.

2. Dynamic
   
   In this state,
   
   - the `size`, `width` and `height` properties evaluate to a [`Size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size "term_image.image.Size") enum member,
   
   - the size with which the image is rendered is automatically calculated (based on the current [terminal size](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-size) or the image’s original size) whenever the image is to be rendered.

The size of an image can be set at instantiation by passing an integer or a [`Size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size "term_image.image.Size") enum member to **either** the *width* **or** the *height* **keyword-only** parameter. For whichever axis a dimension is given, the dimension on the other axis is calculated **proportionally**.

Note

1. The arguments can only be given **by keyword**.

2. If neither is given, the [`FIT`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size.FIT "term_image.image.Size.FIT") [dynamic size](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-size) applies.

3. All methods of instantiation accept these arguments.

For example:

from term_image.image import Size, from_file
image = from_file("python.png")  # Dynamic FIT
image.size is Size.FIT
True
image = from_file("python.png", width=60)  # Fixed
image.size
(60, 30)
image.height
30
image = from_file("python.png", height=56)  # Fixed
image.size
(112, 56)
image.width
112
image = from_file("python.png", height=Size.FIT)  # Fixed FIT
image.size
(136, 68)
image = from_file("python.png", width=Size.FIT_TO_WIDTH)  # Fixed FIT_TO_WIDTH
image.size
(255, 128)
image = from_file("python.png", height=Size.ORIGINAL)  # Fixed ORIGINAL
image.size
(288, 144)

No size validation is performed i.e the resulting size might not fit into the terminal window

image = from_file("python.png", height=68)  # Will fit in, OK
image.size
(136, 68)
image = from_file("python.png", height=500)  # Will not fit in, also OK
image.size
(1000, 500)

An exception is raised when both *width* and *height* are given.

image = from_file("python.png", width=100, height=100)
Traceback (most recent call last):
  .
  .
  .
ValueError: Cannot specify both width and height

The [`width`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.width "term_image.image.BaseImage.width") and [`height`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.height "term_image.image.BaseImage.height") properties can be used to set the size of an image after instantiation, resulting in [fixed size](https://term-image.readthedocs.io/en/stable/glossary.html#term-fixed-size).

image = from_file("python.png")
image.width = 56
image.size
(56, 28)
image.height
28
image.height = 68
image.size
(136, 68)
image.width
136

# Even though the terminal can't contain the resulting height, the size is still set

image.width = 200
image.size
(200, 100)
image.width = Size.FIT
image.size
(136, 69)
image.height = Size.FIT_TO_WIDTH
image.size
(255, 128)
image.height = Size.ORIGINAL
image.size
(288, 144)

The [`size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.size "term_image.image.BaseImage.size") property can only be set to a [`Size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size "term_image.image.Size") enum member, resulting in [dynamic size](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-size).

image = from_file("python.png")
image.size = Size.FIT
image.size is image.width is image.height is Size.FIT
True
image.size = Size.FIT_TO_WIDTH
image.size is image.width is image.height is Size.FIT_TO_WIDTH
True
image.size = Size.ORIGINAL
image.size is image.width is image.height is Size.ORIGINAL
True

Important

1. The currently set [cell ratio](https://term-image.readthedocs.io/en/stable/glossary.html#term-cell-ratio) is also taken into consideration when calculating sizes for images of [Text-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#text-based).

2. There is a **2-line** difference between the **default** [frame size](https://term-image.readthedocs.io/en/stable/glossary.html#term-frame-size) and the terminal size to allow for shell prompts and the likes.

Tip

See [`set_size()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.set_size "term_image.image.BaseImage.set_size") for extended sizing control.

To explore more of the library’s features and functionality, check out the [User Guide](https://term-image.readthedocs.io/en/stable/guide/index.html) and the [API Reference](https://term-image.readthedocs.io/en/stable/api/index.html).



# User Guide

Sub-sections

- [Concepts](https://term-image.readthedocs.io/en/stable/guide/concepts.html)
  - [Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#render-styles)
  - [Auto Cell Ratio](https://term-image.readthedocs.io/en/stable/guide/concepts.html#auto-cell-ratio)
  - [The Active Terminal](https://term-image.readthedocs.io/en/stable/guide/concepts.html#the-active-terminal)
  - [Terminal Queries](https://term-image.readthedocs.io/en/stable/guide/concepts.html#terminal-queries)
- [Render Formatting](https://term-image.readthedocs.io/en/stable/guide/formatting.html)
  - [Padding](https://term-image.readthedocs.io/en/stable/guide/formatting.html#padding)
  - [Alignment](https://term-image.readthedocs.io/en/stable/guide/formatting.html#alignment)
  - [Transparency](https://term-image.readthedocs.io/en/stable/guide/formatting.html#transparency)
  - [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#render-format-specification)

# Concepts

## Render Styles

See [render style](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-style).

All render style classes are designed to share a common interface (with some having extensions), making the usage of one class directly compatible with another, except when using style-specific features.

Hence, the factory functions [`AutoImage`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.AutoImage "term_image.image.AutoImage"), [`from_file`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_file "term_image.image.from_file") and [`from_url`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_url "term_image.image.from_url") provide a means of render-style-agnostic usage of the library. These functions automatically detect the best render style supported by the [active terminal](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal).

There are two main categories of render styles:

### Text-based Render Styles

Represent images using ASCII or Unicode symbols, and in some cases, with escape sequences to reproduce color.

Render style classes in this category are subclasses of [`TextImage`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.TextImage "term_image.image.TextImage"). These include:

- [`BlockImage`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BlockImage "term_image.image.BlockImage")

### Graphics-based Render Styles

Represent images with actual pixels, using terminal graphics protocols.

Render style classes in this category are subclasses of [`GraphicsImage`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.GraphicsImage "term_image.image.GraphicsImage"). These include:

- [`KittyImage`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.KittyImage "term_image.image.KittyImage")

- [`ITerm2Image`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image "term_image.image.ITerm2Image")

### Render Methods

A [render style](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-style) may implement multiple [render methods](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-methods). See the **Render Methods** section in the description of a render style class (that implements multiple render methods), for the description of its render methods.

## Auto Cell Ratio

Note

This concerns [Text-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#text-based) only.

The is a feature which when supported, can be used to determine the [cell ratio](https://term-image.readthedocs.io/en/stable/glossary.html#term-cell-ratio) directly from the terminal emulator itself. With this feature, it is possible to always produce images of text-based render styles with correct **aspect ratio**.

When using either mode of [`AutoCellRatio`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio "term_image.AutoCellRatio"), it’s important to note that some terminal emulators (most non-graphics-capable ones) might have queried. See [Terminal Queries](https://term-image.readthedocs.io/en/stable/guide/concepts.html#terminal-queries).

If the program will never expect any useful input, particularly **while an image’s size is being set/calculated**, then using [`DYNAMIC`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio.DYNAMIC "term_image.AutoCellRatio.DYNAMIC") mode is OK. For an image with [dynamic size](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-size), this includes when it’s being rendered and when its [`rendered_size`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_size "term_image.image.BaseImage.rendered_size"), [`rendered_width`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_width "term_image.image.BaseImage.rendered_width") or [`rendered_height`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_height "term_image.image.BaseImage.rendered_height") property is invoked.

Otherwise i.e if the program will be expecting input, use [`FIXED`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio.FIXED "term_image.AutoCellRatio.FIXED") mode and use [`read_tty_all()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.read_tty_all "term_image.utils.read_tty_all") to read all currently unread input just before calling [`set_cell_ratio()`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.set_cell_ratio "term_image.set_cell_ratio").

## The Active Terminal

See [active terminal](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal).

The following streams/files are checked in the following order (along with the rationale behind the ordering):

- `STDOUT`: Since it’s where images will most likely be drawn.

- `STDIN`: If output is redirected to a file or pipe and the input is a terminal, then using it as the [active terminal](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal) should give the expected result i.e the same as when output is not redirected.

- `STDERR`: If both output and input are redirected, it’s usually unlikely for errors to be.

- `/dev/tty`: Finally, if all else fail, fall back to the process’ controlling terminal, if any.

The first one that is ascertained to be a terminal device is used for all [Terminal Queries](https://term-image.readthedocs.io/en/stable/guide/concepts.html#terminal-queries) and to retrieve the terminal (and window) size on some terminal emulators.

Note

If none of the streams/files is a TTY device, then a [`TermImageWarning`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.TermImageWarning "term_image.exceptions.TermImageWarning") is issued and dependent functionality is disabled.

## Terminal Queries

Some features of this library require the acquisition of certain information from the [active terminal](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal). A single iteration of this acquisition procedure is called a **query**.

A query involves three major steps:

1. Clear all unread input from the terminal

2. Write to the terminal

3. Read from the terminal

For this procedure to be successful, it must not be interrupted.

About #1

If the program is expecting input, use [`read_tty_all()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.read_tty_all "term_image.utils.read_tty_all") to read all currently unread input (**without blocking**) just before any operation involving a query.

About #2 and #3

After sending a request to the terminal, its response is awaited. The default wait time is [`DEFAULT_QUERY_TIMEOUT`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.DEFAULT_QUERY_TIMEOUT "term_image.DEFAULT_QUERY_TIMEOUT") but can be changed using [`set_query_timeout()`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.set_query_timeout "term_image.set_query_timeout"). If the terminal emulator responds after the set timeout, this can result in the application program receiving what would seem to be garbage or ghost input (see this [FAQ](https://term-image.readthedocs.io/en/stable/faqs.html#query-timeout-faq)).

If the program includes any other function that could write to the terminal OR especially, read from the terminal or modify it’s attributes, while a query is in progress (as a result of asynchronous execution e.g multithreading or multiprocessing), decorate it with [`lock_tty()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.lock_tty "term_image.utils.lock_tty") to ensure it doesn’t interfere.

For example, an [image viewer](https://github.com/AnonymouX47/termvisage) based on this project uses [urwid](https://urwid.org/) which reads from the terminal using `urwid.raw_display.Screen.get_available_raw_input()`. To prevent this method from interfering with terminal queries, it uses [`UrwidImageScreen`](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen "term_image.widget.UrwidImageScreen") which overrides and wraps the method like:

class UrwidImageScreen(Screen):
    @lock_tty
    def get_available_raw_input(self):
       return super().get_available_raw_input()

Also, if the [active terminal](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal) is not the controlling terminal of the process using this library (e.g output is redirected to another TTY device), ensure no process that can interfere with a query (e.g a shell or REPL) is currently running in the active terminal. For instance, such a process can be temporarily put to sleep.

### Features that require terminal queries

In parentheses are the outcomes when the terminal doesn’t support queries or when queries are disabled.

- [Auto Cell Ratio](https://term-image.readthedocs.io/en/stable/guide/concepts.html#auto-cell-ratio) (determined to be unsupported)

- Support checks for [Graphics-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#graphics-based) (determined to be unsupported)

- Auto background color (black is used)

- Alpha blend for pixels above the alpha threshold in transparent renders with [Text-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#text-based) (black is used)

- Workaround for ANSI background colors in text-based renders on the Kitty terminal (the workaround is disabled)

Note

This list might not always be complete. In case you notice

- any difference with any unlisted feature when terminal queries are enabled versus when disabled, or

- a behaviour different from the one specified for the listed features, when terminal queries are disabled,

please open an issue [here](https://github.com/AnonymouX47/term-image/issues).





# Render Formatting

Render formatting is simply the modification of a primary [render](https://term-image.readthedocs.io/en/stable/glossary.html#term-render) output. This is provided via:

- Python’s string formatting protocol by using [`format()`](https://docs.python.org/3/library/functions.html#format "(in Python v3.12)"), [`str.format()`](https://docs.python.org/3/library/stdtypes.html#str.format "(in Python v3.12)") or [formatted string literals](https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals) with the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)

- Parameters of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw")

The following constitute render formatting:

## Padding

This adds whitespace around a primary [render](https://term-image.readthedocs.io/en/stable/glossary.html#term-render) output. The amount of whitespace added is determined by two values (with respect to the rendered size):

- [padding width](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-width), determines horizontal padding
  
  - uses the `width` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *pad_width* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw")

- [padding height](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-height), determines vertical padding
  
  - uses the `height` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *pad_height* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw")

If the padding width or height is less than or equal to the width or height of the primary render output, then the padding has no effect on the corresponding axis.

## Alignment

This determines the position of a primary [render](https://term-image.readthedocs.io/en/stable/glossary.html#term-render) output within it’s [Padding](https://term-image.readthedocs.io/en/stable/guide/formatting.html#padding). The position is determined by two values:

- [horizontal alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment), determines the horizontal position
  
  - uses the `h_align` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *h_align* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw")

- [vertical alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment), determines the vertical position
  
  - uses the `v_align` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *v_align* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw")

## Transparency

This determines how transparent pixels are rendered. Transparent pixels can be rendered in one of the following ways:

- Transparency disabled
  
  Alpha channel is ignored.
  
  - uses the `#` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec), without `threshold` or `bgcolor`
  
  - uses the *alpha* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw"), set to `None`

- Transparency enabled with an [alpha threshold](https://term-image.readthedocs.io/en/stable/glossary.html#term-alpha-threshold)
  
  For [Text-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#text-based), any pixel with an alpha value above the given threshold is taken as **opaque**. For [Graphics-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#graphics-based), the alpha value of each pixel is used as-is.
  
  - uses the `threshold` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *alpha* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw"), set to a [`float`](https://docs.python.org/3/library/functions.html#float "(in Python v3.12)") value

- Transparent pixels overlaid on a color
  
  May be specified to be a specific color or the default background color of the terminal emulator (if it can’t be determined, black is used).
  
  - uses the `bgcolor` field of the [Render Format Specification](https://term-image.readthedocs.io/en/stable/guide/formatting.html#format-spec)
  
  - uses the *alpha* parameter of [`draw()`](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw "term_image.image.BaseImage.draw"), set to a string value

## Render Format Specification

[ <h_align> ]  [ <width> ]  [ . [ <v_align> ] [ <height> ] ]  [ # [ <threshold> | <bgcolor> ] ]  [ + <style> ]

Note

- spaces are only for clarity and not included in the syntax

- `<...>` is a placeholder for a single field

- `|` implies mutual exclusivity

- fields within `[ ]` are optional

- fields within `{ }` are required, though subject to any enclosing `[ ]`

- if the `.` is present, then at least one of `v_align` and `height` must be present

- `h_align` → [horizontal alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment)
  
  - `<` → left
  
  - `|` → center
  
  - `>` → right
  
  - *default* → center

- `width` → [padding width](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-width)
  
  - positive integer
  
  - *default*: [terminal width](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-width)
  
  - if **less than or equal** to the [rendered width](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered-width), it has **no effect**

- `v_align` → [vertical alignment](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment)
  
  - `^` → top
  
  - `-` → middle
  
  - `_` → bottom
  
  - *default* → middle

- `height` → [padding height](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-height)
  
  - positive integer
  
  - *default*: [terminal height](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-height) minus two (`2`)
  
  - if **less than or equal** to the [rendered height](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered-height), it has **no effect**

- `#` → transparency setting
  
  - *default*: transparency is enabled with the default [alpha threshold](https://term-image.readthedocs.io/en/stable/glossary.html#term-alpha-threshold)
  
  - `threshold` → [alpha threshold](https://term-image.readthedocs.io/en/stable/glossary.html#term-alpha-threshold)
    
    - a float value in the range `0.0` <= `threshold` < `1.0` (but starting with the `.` (decimal point))
    
    - **applies to only** [Text-based Render Styles](https://term-image.readthedocs.io/en/stable/guide/concepts.html#text-based)
    
    - e.g `.0`, `.325043`, `.999`
  
  - `bgcolor` → background underlay color
    
    - `#` → the terminal emulator’s default background color (or black, if undetermined), OR
    
    - a hex color e.g `ffffff`, `7faa52`
  
  - if neither `threshold` nor `bgcolor` is present, but `#` is present, transparency is disabled i.e alpha channel is ignored

- `style` → style-specific format specifier
  
  See each render style in [Image Classes](https://term-image.readthedocs.io/en/stable/api/image.html#image-classes) for its own specification, if it defines.
  
  `style` can be broken down into `[ <parent> ] [ <current> ]`, where `current` is the spec defined by a render style and `parent` is the spec defined by a parent of that render style. `parent` can in turn be **recursively** broken down as such.

See also

[Formatted rendering](https://term-image.readthedocs.io/en/stable/start/tutorial.html#formatted-render) tutorial.





# API Reference

Attention

🚧 Under Construction - There might be incompatible interface changes between minor versions of [version zero](https://semver.org/spec/v2.0.0.html#spec-item-4)!

If you want to use the library in a project while it’s still on version zero, ensure you pin the dependency to a specific minor version e.g `>=0.4,<0.5`.

On this note, you probably also want to switch to the specific documentation for the version you’re using (somewhere at the lower left corner of this page).

Attention

Any module or definition not documented here should be considered part of the private interface and can be changed or removed at any time without notice.

Sub-sections:

- [Top-Level Definitions](https://term-image.readthedocs.io/en/stable/api/toplevel.html)
  - [Constants](https://term-image.readthedocs.io/en/stable/api/toplevel.html#constants)
  - [Enumerations](https://term-image.readthedocs.io/en/stable/api/toplevel.html#enumerations)
  - [Functions](https://term-image.readthedocs.io/en/stable/api/toplevel.html#functions)
- [`image` Module](https://term-image.readthedocs.io/en/stable/api/image.html)
  - [Functions](https://term-image.readthedocs.io/en/stable/api/image.html#functions)
  - [Enumerations](https://term-image.readthedocs.io/en/stable/api/image.html#enumerations)
  - [Image Classes](https://term-image.readthedocs.io/en/stable/api/image.html#image-classes)
  - [Other Classes](https://term-image.readthedocs.io/en/stable/api/image.html#other-classes)
- [`widget` Module](https://term-image.readthedocs.io/en/stable/api/widget.html)
  - [`UrwidImage`](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImage)
  - [`UrwidImageCanvas`](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageCanvas)
  - [`UrwidImageScreen`](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen)
- [`exceptions` Module](https://term-image.readthedocs.io/en/stable/api/exceptions.html)
  - [`TermImageWarning`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.TermImageWarning)
  - [`TermImageError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.TermImageError)
  - [`InvalidSizeError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.InvalidSizeError)
  - [`RenderError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.RenderError)
  - [`StyleError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.StyleError)
  - [`URLNotFoundError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.URLNotFoundError)
  - [`UrwidImageError`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.UrwidImageError)
- [`utils` Module](https://term-image.readthedocs.io/en/stable/api/utils.html)
  - [`get_cell_size()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_cell_size)
  - [`get_terminal_name_version()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_terminal_name_version)
  - [`get_terminal_size()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_terminal_size)
  - [`lock_tty()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.lock_tty)
  - [`read_tty_all()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.read_tty_all)
  - [`write_tty()`](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.write_tty)

[

Next

Top-Level Definitions

](https://term-image.readthedocs.io/en/stable/api/toplevel.html)[

Previous

Render Formatting

](https://term-image.readthedocs.io/en/stable/guide/formatting.html)

Copyright © 2022, Toluwaleke Ogundipe

Made with [Sphinx](https://www.sphinx-doc.org/) and [@pradyunsg](https://pradyunsg.me/)'s [Furo](https://github.com/pradyunsg/furo)

[](https://readthedocs.org/projects/term-image)[](https://github.com/AnonymouX47/term-image)





# Index

[**A**](https://term-image.readthedocs.io/en/stable/genindex.html#A) | [**B**](https://term-image.readthedocs.io/en/stable/genindex.html#B) | [**C**](https://term-image.readthedocs.io/en/stable/genindex.html#C) | [**D**](https://term-image.readthedocs.io/en/stable/genindex.html#D) | [**E**](https://term-image.readthedocs.io/en/stable/genindex.html#E) | [**F**](https://term-image.readthedocs.io/en/stable/genindex.html#F) | [**G**](https://term-image.readthedocs.io/en/stable/genindex.html#G) | [**H**](https://term-image.readthedocs.io/en/stable/genindex.html#H) | [**I**](https://term-image.readthedocs.io/en/stable/genindex.html#I) | [**J**](https://term-image.readthedocs.io/en/stable/genindex.html#J) | [**K**](https://term-image.readthedocs.io/en/stable/genindex.html#K) | [**L**](https://term-image.readthedocs.io/en/stable/genindex.html#L) | [**M**](https://term-image.readthedocs.io/en/stable/genindex.html#M) | [**N**](https://term-image.readthedocs.io/en/stable/genindex.html#N) | [**O**](https://term-image.readthedocs.io/en/stable/genindex.html#O) | [**P**](https://term-image.readthedocs.io/en/stable/genindex.html#P) | [**R**](https://term-image.readthedocs.io/en/stable/genindex.html#R) | [**S**](https://term-image.readthedocs.io/en/stable/genindex.html#S) | [**T**](https://term-image.readthedocs.io/en/stable/genindex.html#T) | [**U**](https://term-image.readthedocs.io/en/stable/genindex.html#U) | [**V**](https://term-image.readthedocs.io/en/stable/genindex.html#V) | [**W**](https://term-image.readthedocs.io/en/stable/genindex.html#W)

## A

| - [**active terminal**](https://term-image.readthedocs.io/en/stable/glossary.html#term-active-terminal)<br>- [**alignment**](https://term-image.readthedocs.io/en/stable/glossary.html#term-alignment)<br>- [**alpha threshold**](https://term-image.readthedocs.io/en/stable/glossary.html#term-alpha-threshold)<br>- [**animated**](https://term-image.readthedocs.io/en/stable/glossary.html#term-animated)<br>- [AUTO (term_image.image.Size attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size.AUTO) | - [auto_image_class() (in module term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.auto_image_class)<br>- [AutoCellRatio (class in term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio)<br>- [AutoImage() (in module term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.AutoImage)<br>- [**automatic size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-automatic-size)<br>- [**automatic sizing**](https://term-image.readthedocs.io/en/stable/glossary.html#term-automatic-sizing) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## B

| - [BaseImage (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage) | - [BlockImage (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BlockImage) |
| -------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |

## C

| - [**cell ratio**](https://term-image.readthedocs.io/en/stable/glossary.html#term-cell-ratio)<br>- [clear() (term_image.image.ITerm2Image class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image.clear)<br>  - [(term_image.image.KittyImage class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.KittyImage.clear) | - [clear_images() (term_image.widget.UrwidImageScreen method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen.clear_images)<br>- [close() (term_image.image.BaseImage method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.close)<br>  - [(term_image.image.ImageIterator method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageIterator.close)<br>- [closed (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.closed) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## D

| - [DEFAULT_QUERY_TIMEOUT (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.DEFAULT_QUERY_TIMEOUT)<br>- [**descendant**](https://term-image.readthedocs.io/en/stable/glossary.html#term-descendant)<br>- [disable_queries() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.disable_queries)<br>- [disable_win_size_swap() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.disable_win_size_swap) | - [draw() (term_image.image.BaseImage method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.draw)<br>- [draw_screen() (term_image.widget.UrwidImageScreen method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen.draw_screen)<br>- [DYNAMIC (term_image.AutoCellRatio attribute)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio.DYNAMIC)<br>- [**dynamic size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-size)<br>- [**dynamic sizing**](https://term-image.readthedocs.io/en/stable/glossary.html#term-dynamic-sizing) |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## E

| - [enable_queries() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.enable_queries) | - [enable_win_size_swap() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.enable_win_size_swap) |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |

## F

| - [FILE_PATH (term_image.image.ImageSource attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageSource.FILE_PATH)<br>- [FIT (term_image.image.Size attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size.FIT)<br>- [FIT_TO_WIDTH (term_image.image.Size attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size.FIT_TO_WIDTH)<br>- [FIXED (term_image.AutoCellRatio attribute)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio.FIXED)<br>- [**fixed size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-fixed-size)<br>- [**fixed sizing**](https://term-image.readthedocs.io/en/stable/glossary.html#term-fixed-sizing)<br>- [flush() (term_image.widget.UrwidImageScreen method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen.flush)<br>- [forced_support (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.forced_support) | - [**frame height**](https://term-image.readthedocs.io/en/stable/glossary.html#term-frame-height)<br>- [**frame size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-frame-size)<br>- [**frame width**](https://term-image.readthedocs.io/en/stable/glossary.html#term-frame-width)<br>- [frame_duration (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.frame_duration)<br>- [from_file() (in module term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_file)<br>  - [(term_image.image.BaseImage class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.from_file)<br>- [from_url() (in module term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.from_url)<br>  - [(term_image.image.BaseImage class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.from_url) |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## G

| - [get_available_raw_input() (term_image.widget.UrwidImageScreen method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen.get_available_raw_input)<br>- [get_cell_ratio() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.get_cell_ratio)<br>- [get_cell_size() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_cell_size) | - [get_terminal_name_version() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_terminal_name_version)<br>- [get_terminal_size() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.get_terminal_size)<br>- [GraphicsImage (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.GraphicsImage) |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## H

| - [height (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.height) | - [**horizontal alignment**](https://term-image.readthedocs.io/en/stable/glossary.html#term-horizontal-alignment) |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |

## I

| - [image (term_image.widget.UrwidImage property)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImage.image)<br>- [ImageIterator (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageIterator)<br>- [ImageSource (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageSource)<br>- [InvalidSizeError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.InvalidSizeError) | - [is_animated (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.is_animated)<br>- [is_supported (term_image.AutoCellRatio attribute)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.AutoCellRatio.is_supported)<br>- [is_supported() (term_image.image.BaseImage class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.is_supported)<br>- [ITerm2Image (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## J

- [jpeg_quality (term_image.image.ITerm2Image property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image.jpeg_quality)

## K

- [KittyImage (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.KittyImage)

## L

| - [lock_tty() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.lock_tty) | - [loop_no (term_image.image.ImageIterator property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageIterator.loop_no) |
| --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |

## M

- [**manual size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-manual-size)
- [**manual sizing**](https://term-image.readthedocs.io/en/stable/glossary.html#term-manual-sizing)
- module
  - [term_image](https://term-image.readthedocs.io/en/stable/api/toplevel.html#module-term_image)
  - [term_image.exceptions](https://term-image.readthedocs.io/en/stable/api/exceptions.html#module-term_image.exceptions)
  - [term_image.image](https://term-image.readthedocs.io/en/stable/api/image.html#module-term_image.image)
  - [term_image.utils](https://term-image.readthedocs.io/en/stable/api/utils.html#module-term_image.utils)
  - [term_image.widget](https://term-image.readthedocs.io/en/stable/api/widget.html#module-term_image.widget)

## N

| - [n_frames (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.n_frames) | - [native_anim_max_bytes (term_image.image.ITerm2Image property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image.native_anim_max_bytes) |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## O

| - [ORIGINAL (term_image.image.Size attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size.ORIGINAL) | - [original_size (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.original_size) |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |

## P

| - [**padding**](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding)<br>- [**padding height**](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-height) | - [**padding width**](https://term-image.readthedocs.io/en/stable/glossary.html#term-padding-width)<br>- [PIL_IMAGE (term_image.image.ImageSource attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageSource.PIL_IMAGE)<br>- [**pixel ratio**](https://term-image.readthedocs.io/en/stable/glossary.html#term-pixel-ratio) |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## R

| - [read_from_file (term_image.image.ITerm2Image property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ITerm2Image.read_from_file)<br>- [read_tty_all() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.read_tty_all)<br>- [**render**](https://term-image.readthedocs.io/en/stable/glossary.html#term-render)<br>- [**render method**](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-method)<br>- [**render methods**](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-methods)<br>- [**render style**](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-style)<br>- [**render styles**](https://term-image.readthedocs.io/en/stable/glossary.html#term-render-styles)<br>- [**rendered**](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered) | - [**rendered height**](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered-height)<br>- [**rendered size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered-size)<br>- [**rendered width**](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendered-width)<br>- [rendered_height (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_height)<br>- [rendered_size (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_size)<br>- [rendered_width (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.rendered_width)<br>- [RenderError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.RenderError)<br>- [**rendering**](https://term-image.readthedocs.io/en/stable/glossary.html#term-rendering) |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## S

| - [seek() (term_image.image.BaseImage method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.seek)<br>  - [(term_image.image.ImageIterator method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageIterator.seek)<br>- [set_cell_ratio() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.set_cell_ratio)<br>- [set_error_placeholder() (term_image.widget.UrwidImage class method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImage.set_error_placeholder)<br>- [set_query_timeout() (in module term_image)](https://term-image.readthedocs.io/en/stable/api/toplevel.html#term_image.set_query_timeout)<br>- [set_render_method() (term_image.image.BaseImage class method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.set_render_method)<br>- [set_size() (term_image.image.BaseImage method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.set_size) | - [Size (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.Size)<br>- [size (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.size)<br>- [**source**](https://term-image.readthedocs.io/en/stable/glossary.html#term-source)<br>  - [(term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.source)<br>- [source_type (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.source_type)<br>- [**style**](https://term-image.readthedocs.io/en/stable/glossary.html#term-style)<br>- [StyleError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.StyleError)<br>- [**styles**](https://term-image.readthedocs.io/en/stable/glossary.html#term-styles) |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## T

| - [tell() (term_image.image.BaseImage method)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.tell)<br>- term_image<br>  - [module](https://term-image.readthedocs.io/en/stable/api/toplevel.html#module-term_image)<br>- term_image.exceptions<br>  - [module](https://term-image.readthedocs.io/en/stable/api/exceptions.html#module-term_image.exceptions)<br>- term_image.image<br>  - [module](https://term-image.readthedocs.io/en/stable/api/image.html#module-term_image.image)<br>- term_image.utils<br>  - [module](https://term-image.readthedocs.io/en/stable/api/utils.html#module-term_image.utils) | - term_image.widget<br>  - [module](https://term-image.readthedocs.io/en/stable/api/widget.html#module-term_image.widget)<br>- [TermImageError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.TermImageError)<br>- [TermImageWarning](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.TermImageWarning)<br>- [**terminal height**](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-height)<br>- [**terminal size**](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-size)<br>- [**terminal width**](https://term-image.readthedocs.io/en/stable/glossary.html#term-terminal-width)<br>- [TextImage (class in term_image.image)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.TextImage) |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

## U

| - [URL (term_image.image.ImageSource attribute)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.ImageSource.URL)<br>- [URLNotFoundError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.URLNotFoundError)<br>- [UrwidImage (class in term_image.widget)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImage) | - [UrwidImageCanvas (class in term_image.widget)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageCanvas)<br>- [UrwidImageError](https://term-image.readthedocs.io/en/stable/api/exceptions.html#term_image.exceptions.UrwidImageError)<br>- [UrwidImageScreen (class in term_image.widget)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen) |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |

## V

- [**vertical alignment**](https://term-image.readthedocs.io/en/stable/glossary.html#term-vertical-alignment)

## W

| - [width (term_image.image.BaseImage property)](https://term-image.readthedocs.io/en/stable/api/image.html#term_image.image.BaseImage.width) | - [write() (term_image.widget.UrwidImageScreen method)](https://term-image.readthedocs.io/en/stable/api/widget.html#term_image.widget.UrwidImageScreen.write)<br>- [write_tty() (in module term_image.utils)](https://term-image.readthedocs.io/en/stable/api/utils.html#term_image.utils.write_tty) |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |







# Python Module Index

[**t**](https://term-image.readthedocs.io/en/stable/py-modindex.html#cap-t)

|                                                                     |                                                                                                                         |     |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --- |
|                                                                     | **t**                                                                                                                   |     |
| ![-](https://term-image.readthedocs.io/en/stable/_static/minus.png) | [`term_image`](https://term-image.readthedocs.io/en/stable/api/toplevel.html#module-term_image)                         |     |
|                                                                     | [`term_image.exceptions`](https://term-image.readthedocs.io/en/stable/api/exceptions.html#module-term_image.exceptions) |     |
|                                                                     | [`term_image.image`](https://term-image.readthedocs.io/en/stable/api/image.html#module-term_image.image)                |     |
|                                                                     | [`term_image.utils`](https://term-image.readthedocs.io/en/stable/api/utils.html#module-term_image.utils)                |     |
|                                                                     | [`term_image.widget`](https://term-image.readthedocs.io/en/stable/api/widget.html#module-term_image.widget)             |     |





## Features

[](https://github.com/AnonymouX47/term-image#features)

- Multiple image formats (basically all formats supported by [`PIL.Image.open()`](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html))
- Multiple image source types: PIL image instance, local file, URL
- Multiple image render styles (with automatic support detection)
- Support for multiple terminal graphics protocols: [Kitty](https://sw.kovidgoyal.net/kitty/graphics-protocol/), [iTerm2](https://iterm2.com/documentation-images.html)
  - Exposes various features of the protocols
- Transparency support (with multiple options)
- Animated image support (including transparent ones)
  - Multiple formats: GIF, WEBP, APNG (and possibly more)
  - Fully controllable iteration over rendered frames of animated images
  - Image animation with multiple parameters
- Integration into various TUI / terminal-based output libraries.
- Terminal size awareness
- Automatic and manual image sizing
- Horizontal and vertical alignment
- Automatic and manual font ratio adjustment (to preserve image aspect ratio)
- and more... 😁
