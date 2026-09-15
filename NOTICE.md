# Third-party components

JioLite packages a focused copy of these upstream projects for its local runtime:

- OrpheusDL core: <https://github.com/OrfiTeam/OrpheusDL>, based on commit
  `a45ff47913508d4c09971bdb847d5845984f1e64`.
- JioSaavn module: <https://github.com/bunnykek/orpheusdl-jiosaavn>, based on
  commit `0c20361935f83c61972b7eddccda446be57090ec`.

The packaged copies include local fixes for Saavn CDN referrer handling,
high-resolution artwork URL construction, and HTTP error validation.

Neither checked-out upstream repository included a license file. Confirm the
upstream redistribution terms before publishing this package publicly. A
private repository for personal synchronization avoids public redistribution.
