# wpgtk-firefox-themer

This script allows you to apply your color schemes from [wpgtk](https://github.com/deviantfero/wpgtk) or [pywal](https://github.com/dylanaraps/pywal) to Firefox and Thunderbird using the official [Firefox Color addon](https://addons.mozilla.org/en-GB/firefox/addon/firefox-color/).

## Setup

1. Install [msgpack](https://pypi.org/project/msgpack/) using either pip or your distro's package manager (`sudo apt install python3-msgpack` on Debian/Ubuntu, for example)
2. Copy `theme.json.example` to `theme.json`, and make some adjustments if you want (see Configuration below)
3. Run `wpgtk-firefox-themer.py` to get the Firefox Color URL
4. Open it in Firefox or Thunderbird, install the addon if you haven't yet, and confirm the popup asking whether you want to apply the new theme

## Help

    Usage: wpgtk-firefox-themer.py [mode or Firefox Color URL]

    Modes:
      url     Default. Output the Firefox Color URL to stdout
      ff      Open the Firefox Color URL in default browser (probably Firefox)
      tb      Open a message containing the URL in Thunderbird (thunderbird must be in PATH, and should already be open)

    If a Firefox Color URL is passed as the argument, it will be decoded into JSON as a base to build your own theme config off of.

## Installing Firefox Color in Thunderbird

Since you can't just open a browser tab in Thunderbird or install Firefox addons there, running the script with the `tb` argument will instead open a message containg the link. You can open the page this way and install the addon from there. Make sure to disable any themes you might have installed previously, as they might override the Firefox Color theme when starting the application.

If you have set Thunderbird to open links in your browser, consider installing the [Open Tab addon](https://addons.thunderbird.net/en-US/thunderbird/addon/open-tab/), which adds a context menu option to open a browser tab in Thunderbird when right-clicking a link.

## Configuration

You can edit the `theme.json` file to change which element uses which color from the scheme. Every key in the `colors` object should have a string value, which can be:
- `color0` to `color15`, `background`, `foreground` or `cursor`, which are replaced with the corresponding color from your scheme
- Any keyword defined in wpgtk that resolves to a hex color code (#xxxxxx)
- A fixed color as a hex code (#xxxxxx)

The values for the `images` and `title` will be carried over to the theme without changes.

If you already have a Firefox Color theme and want to use images from there, or want to experiment to see which property corresponds to which color on the site, you can convert any theme from the site to JSON by clicking on the Export button on the top right, and using that URL as an argument for the script.

## Firefox Color URLs

Firefox Color uses the [json-url npm package](https://www.npmjs.com/package/json-url) for the theme parameter in the URL. It first uses msgpack to pack the theme object, then compresses it using lzma and encodes the data using URL-safe base64. The URL-safe base64 used is similar to the Python one, with `+` being replaced by `-` and `/` being replaced by `_`, but also removes all of the `=` padding at the end.

This script leaves the padding when encoding, as it still works correctly. When decoding an existing theme, the script simply adds the maximum number of `=` to the end of the base64 data instead of the exactly correct amount, as the Python implementation ignores excessive padding.
