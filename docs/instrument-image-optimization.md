Instrument images optimization

What I did

- Backed up original high-resolution images from `static/images/instruments` to `assets/images/instruments/originals/`.
- Resized the JPEGs (maximum dimension 1200px) and overwrote the files in `static/images/instruments`.
- Created WebP equivalents at quality 75 alongside the JPEGs.
- Removed (staged) built copies under `public/images/instruments` to reduce repo size; the next site build will regenerate `public` from `static`.

Why

- Resizing drastically reduces filesize while keeping adequate quality for web display.
- WebP provides additional compression for supported browsers.

To revert

- Originals are in `assets/images/instruments/originals/` — copy them back into `static/images/instruments/` if you want to restore the original files.

Notes

- AVIF encoding was not available on this machine; we used WebP with `cwebp` instead. If you want AVIF, I can install `avifenc` or convert on a system that has it.
- I staged deletions from `public` (run `git status`/`git diff` to review); commit when ready.
