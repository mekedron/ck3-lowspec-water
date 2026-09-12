# Better Water Without Advanced Shaders - options.
#
# This file is new (no vanilla counterpart) and is the first include of
# gfx/FX/pdxwater.shader and gfx/FX/jomini/jomini_water_default.fxh. Comment a line
# out, re-run install.sh and restart the game to fall back to vanilla for that part.

Code
[[
	// The ocean with Advanced Shaders off: two animated wave layers, the sun highlight,
	// the sky reflection through the Fresnel term and deep/shallow colour, instead of
	// the flat colour map. 6 texture taps per pixel; vanilla low spec spends 11.
	#define WATEROPT_CHEAP_WAVES

	// Lakes with Advanced Shaders off take the same cheap water. Vanilla has no low spec
	// lake effect and runs the full ~50 tap water shader on them.
	#define WATEROPT_CHEAP_LAKES
]]
