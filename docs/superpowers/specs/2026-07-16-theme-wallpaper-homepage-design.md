# Theme-aware homepage wallpaper design

## Goal

Replace the circular avatar at the top of the homepage with a large responsive wallpaper. Show `images/洛天依壁纸.png` in the light theme and `images/洛天依壁纸_夜.png` in the dark theme while keeping the existing title, description, and GitHub button below the image.

## Structure

The homepage profile card will contain two image elements before its text content. Each image has a shared wallpaper class and a theme-specific class. The existing Material theme attribute, `data-md-color-scheme`, controls which image is visible.

The light image is visible by default. Under `[data-md-color-scheme="slate"]`, the light image is hidden and the dark image is shown. This follows Material's manual theme toggle as well as its initial theme selection.

## Presentation

- The wallpaper fills the available content width and retains its original aspect ratio without cropping.
- A small border radius softens the image edges.
- The title, description, and GitHub button remain centered below the wallpaper.
- The old circular avatar styling is removed because it no longer has a consumer.
- Mobile layouts use the same responsive image and do not introduce a separate crop.

## Files changed

- `docs/index.md`: replace the avatar element with the two wallpaper elements.
- `docs/resources/css/extra.css`: replace avatar styles with responsive wallpaper and theme-visibility rules.

## Verification

Build the MkDocs site and verify that it completes without warnings. In the rendered homepage, check both Material color schemes and confirm that exactly one correct wallpaper is visible, the image is not distorted, and the content remains below it at desktop and mobile widths.
