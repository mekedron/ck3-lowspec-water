# Better Water Without Advanced Shaders (CK3)

Shaded water on the map when the graphics option **Advanced Shaders** is off. Vanilla
low spec draws the ocean as its colour map with a shore fade and nothing else; this mod
gives it two layers of animated waves, the sun highlight, the sky reflected through the
Fresnel term and the deep/shallow colour shift - the look of the full water shader with
only its cheap parts, at 6 texture taps per pixel where vanilla low spec already spent 11.

<img src="thumbnail.png" alt="The North Sea with Advanced Shaders off: waves, a sun highlight and sky reflection" width="360">

Independent of every other mod; pairs with
[Sharp Terrain Without Advanced Shaders](https://github.com/mekedron/ck3-lowspec-terrain-fix)
and its [Real Snow](https://github.com/mekedron/ck3-lowspec-real-snow) add-on.

## Cause

With Advanced Shaders off the ocean is drawn by `Effect waterLowSpec` in
`game/gfx/FX/pdxwater.shader`. Its pixel shader, `CalcWaterLowSpec`, reads the water
colour map and computes a shore fade - and the fade alone calls `GetHeightMultisample`,
a 9 tap heightmap blur (10 fetches with the indirection lookup). That is all: no
normals, no light, no reflection. Lakes are worse the other way round: they have no low
spec effect at all (`lake`, `lake_mapobject` always use the full `PixelShader`), so a
low spec map draws every lake with the ~50 tap high spec water.

## Fix

`gfx/FX/jomini/jomini_water_default.fxh` gains one function, `CalcWaterCheap`, built
from the pieces of the vanilla `CalcWater` that are cheap:

| kept | dropped |
| --- | --- |
| wave normal layers 1 and 2 (2 taps) | wave layer 3, flow maps (8 taps) |
| sun diffuse + Blinn-Phong highlight, sunny scenario constants | shadow map, cloud mask, dual scenario |
| sky cube map through the Fresnel term (1 tap) | refraction (3 taps + a render pass) |
| deep/shallow colour by view angle, colour map tint | foam (6 taps), approaching shore waves (10 taps) |
| shore fade from one height tap (2 fetches) | the 9 tap height multisample |

`gfx/FX/pdxwater.shader` calls it from `PixelShaderLowSpec` (the ocean) and, when
`LOW_SPEC_SHADERS` is defined, from `PixelShader` (lakes). With Advanced Shaders on
nothing changes. Both switches are in `gfx/FX/better_water_options.fxh`
(`WATEROPT_CHEAP_WAVES`, `WATEROPT_CHEAP_LAKES`); comment one out, re-run
`./install.sh`, restart the game to get vanilla back for that part. Rivers are not
touched: vanilla already draws them with the full water shader in low spec, and they
cover little of the screen.

## Cost

Measured on an RTX 3050 Ti Laptop (4 GB) at 5120x1440 on the North Sea: the low spec
60 FPS held with V-Sync on. Per water pixel the mod does 6 texture taps (height 2,
colour 1, waves 2, cube map 1) against 11 for vanilla low spec, plus the lighting
maths; lakes go from ~50 taps to 6.

## Layout

    descriptor.mod                              mod metadata
    thumbnail.png                               Workshop preview, must sit in the mod root
    gfx/FX/pdxwater.shader                      overrides game/gfx/FX/pdxwater.shader
    gfx/FX/jomini/jomini_water_default.fxh      overrides game/gfx/FX/jomini/jomini_water_default.fxh
    gfx/FX/better_water_options.fxh             the two switches (new file)
    install.sh                                  copies the mod into the Proton prefix
    tools/compile_check.py                      offline compile check with DXC
    tools/check_log.sh                          mount + shader error check after a game start
    tools/diff_vanilla.sh                       re-diff against the Steam files after a patch
    steam-workshop/                             listing texts and the thumbnail generator

## Installing

Run `./install.sh`. It copies the mod into the CK3 mod directory inside the Proton
prefix, then enable "Better Water Without Advanced Shaders" in the launcher playset.
Keep **Advanced Shaders off**; with it on the game uses the high spec water and this
mod changes nothing. The first map load is slower while the shaders compile.

## Verifying without starting the game

    tools/compile_check.py --dxc <dir with bin/dxc and lib/libdxcompiler.so>

takes the vanilla entries of `water`, `waterLowSpec` and `lake` from the game's shader
cache (expanded HLSL), swaps in this mod's code blocks and compiles them with DXC.

## Game version

Built against 1.19.0.6 (Scribe). Both overrides replace the vanilla file wholesale,
so after a patch run `tools/diff_vanilla.sh` and re-apply the banners onto the new
vanilla copies. `jomini_water_default.fxh` is also included by the river shader, which
is why the new function is appended and nothing existing is edited.

## Compatibility

Replaces `gfx/FX/pdxwater.shader` and `gfx/FX/jomini/jomini_water_default.fxh` in
full; conflicts only with mods that edit those files, mostly water or map graphics
overhauls. Fast Advanced Shaders already contains this water - do not combine the two.

## Multiplayer / achievements

Shader files are not checksummed content, but the launcher still marks any mod as a
mod. Treat it like any other graphics mod.
