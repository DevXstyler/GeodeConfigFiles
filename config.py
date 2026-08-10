# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder
from qtile_extras.widget import Visualizer


import subprocess
# Notes:
# |         Note         |      Shortcut         |          Terminal command 
# | Reload Qtile config  | Super + ctrl + r      | qtile cmd-obj -o cmd -f reload_config
#
#
#
#
#a

ctrl = "control" # control key
mod = "mod4" #aka Windows key | Super | Meta | Mod
mod1 = "mod1" #alt key
ctrl = "control"
terminal = "alacritty" #This is an example on how flexible Qtile is, you create variables then use them in a keybind for example
filemanager = "thunar" # Default is thunar






# Sticky windows

sticky_windows = []

@lazy.function
def toggle_sticky_windows(qtile, window=None):
    if window is None:
        window = qtile.current_screen.group.current_window
    if window in sticky_windows:
        sticky_windows.remove(window)
    else:
        sticky_windows.append(window)
    return window

@hook.subscribe.setgroup
def move_sticky_windows():
    for window in sticky_windows:
        window.togroup()
    return

@hook.subscribe.client_killed
def remove_sticky_windows(window):
    if window in sticky_windows:
        sticky_windows.remove(window)

# Below is an example how to make Firefox Picture-in-Picture windows automatically sticky.
@hook.subscribe.client_managed
def auto_sticky_windows(window):
    info = window.info()
    if (info['wm_class'] == ['Toolkit', 'firefox']
            and info['name'] == 'Picture-in-Picture'):
        sticky_windows.append(window)

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█

keys = [                              
    # ▗▄▄▖▗▖ ▗▖ ▗▄▄▖▗▄▄▄▖▗▄▖ ▗▖  ▗▖
    #▐▌   ▐▌ ▐▌▐▌     █ ▐▌ ▐▌▐▛▚▞▜▌
    #▐▌   ▐▌ ▐▌ ▝▀▚▖  █ ▐▌ ▐▌▐▌  ▐▌
    #▝▚▄▄▖▝▚▄▞▘▗▄▄▞▘  █ ▝▚▄▞▘▐▌  ▐▌                            
    # Tiling
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating for focused window"),
    Key([mod, ctrl], "n", lazy.layout.normalize()),


    # Applications
    Key([mod], "m", lazy.window.toggle_minimize(), desc="Minimize/unminimize focused"),
    Key([mod, "shift"], "m", lazy.group.spawn("rofi -show window")),  # optional restore via rofi
    Key([mod], "grave", lazy.screen.toggle_group(), desc="Toggle last group"),

    # Run Apps
    Key([ctrl, "shift"], "Escape", lazy.spawn("btop"), desc="Run btop/taskmgr",),
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle focused window to fullscreen"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod1, "control"], "t", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    # Modified
    Key([mod, "control"], "Delete", lazy.shutdown(), desc="Shutdown Qtile"),

    Key([mod1], "Space", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),

##CUSTOM

    # Modified
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"), desc='volume down'),
    
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc='brightness Down'),
    
##Misc keybinds
    Key([], "Print", lazy.spawn("flameshot gui"), desc='Screenshot'),
    Key(["control"], "Print", lazy.spawn("flameshot full -c -p ~/Pictures/"), desc='Screenshot'),
    
    # Modified
    Key([mod], "e", lazy.spawn(filemanager), desc="Open file manager"),

    # Useful
    Key([mod], "s",toggle_sticky_windows(), desc="Toggle state of sticky for current window"),
]   

# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█


groups = [Group(f"{i+1}", label="■") for i in range(9)] #Be careful modifying this, otherwise qtile config will break ⬤

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )


###𝙇𝙖𝙮𝙤𝙪𝙩###

layouts = [
    layout.Columns(
        margin = 0,
        border_focus = '#C084FC',
        border_normal = '#1F1D2E', 
        border_width = 3,
    ),
    
    layout.Max(
        border_focus = '#C084FC',
        border_normal = '#1F1D2E',
        margin = 0,
        border_width = 0,
    ),
    
    layout.Floating(
        border_focus = '#C084FC',
        border_normal = '#1F1D2E',
        margin = 0,
        border_width = 3,
    ),
    # Try more layouts by unleashing below layouts
   #  layout.Stack(num_stacks=2),
   #  layout.Bsp(),
     layout.Matrix(
        border_focus = '#C084FC',
        border_normal = '#1F1D2E',
        margin = 0,
        border_width = 3,
    ),
     
    layout.MonadWide(
        border_focus = '#C084FC',
        border_normal = '#1F1D2E',
        margin = 0,
        border_width = 3,
    ),
    layout.Tile(
        border_focus = '#C084FC',
        border_normal = '#1F1D2E',
        margin = 0,
        border_width = 3,
    ),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]


widget_defaults = dict(
    font = "DejaVu Sans",
    fontsize = 12,
    padding = 4,
)

extension_defaults = widget_defaults.copy()


def open_launcher():
    qtile.spawn("rofi -show drun")

def open_btop():
    qtile.spawn("alacritty --hold -e btop")


            
# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄
 
screens = [
    Screen(
        top = bar.Bar(
            [   
                widget.Spacer(
                    length = 12,
                    background = '#180F28',
                ),
                
                widget.Image(
                    filename = '~/.config/qtile/Assets/launch_Icon.png',
                    background = '#180F28',
                    # Modified
                    mouse_callbacks = {'Button1': open_launcher,"Button3": open_btop},
                ),

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/6.png',
                #),
                widget.Spacer(length=12, background='#180F28'),

                widget.GroupBox(
                    fontsize = 16,
                    borderwidth = 0,
                    highlight_method = 'line',
                    active = '#7B52C4',                  # active workspace (hover/occupied)
                    block_highlight_text_color = '#4A2D7A',# current workspace circle (darker purple)
                    highlight_color = '#4B427E',         # hover/focus strip (close to palette purple)
                    inactive = '#222D32',                # empty workspace circle (dark bluish gray)
                    foreground = '#180F28',              # text/icon color (very dark purple — probably too dark on dark bg)
                    background = '#180F28',              # panel background (slightly lighter dark)
                    this_current_screen_border = '#FF80E0',# current screen indicator (pink)
                    this_screen_border = '#52548D',      # divider/secondary border (muted indigo)
                    other_current_screen_border = '#52548D',
                    other_screen_border = '#52548D',
                    urgent_border = '#52548D',
                    rounded = False,
                    disable_drag = True,
                ),


                #widget.Image(
                #    filename = '~/.config/qtile/Assets/5.png',
                #),

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/2.png',
                #),
                widget.Spacer(length=15, background='#180F28'),

                widget.CurrentLayout(
                    background ='#4A2D7A',
                    font = 'UNDERWAVE',
                    fontsize = 15,
                    padding = 15,
                ),

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/5.png',                
                #),

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/2.png',
                #),
                widget.Spacer(length=15, background='#180F28'),


                widget.WindowName(
                    background = '#4A2D7A',
                    format = "{name}",
                    align='center',
                    font = 'UNDERWAVE',
                    fontsize = 13,
                    empty_group_string = "Don't be evil, do Open Source | [._.]",
                    padding = 10,
                    max_chars=48,
                ),
                #Visualizer(
                #    bars=8,
                #    width=150,
                #    bar_height=20,
                #    spacing=2,
                #    bar_colour="#ffffff",
                #    framerate=25,
                #    channels="mono",
                #    cava_pipe="/tmp/cava.pipe",  # default cava pipe
                #    cava_path=None,              # set if cava not in PATH
                #    autostart=True,
                #    hide=True,
                #    hide_crash=False,
                #    invert=False,
                #),
                widget.Spacer(
                    length = 10,
                    background = '#4A2D7A',
                ),  
                Visualizer(
                    width=180,
                    bars=16,
                    bar_colour="#180F28",
                    background = "#4A2D7A",
                    margin=4,
                ),
                widget.Spacer(length=40, background='#4A2D7A'),
                #widget.Image(
                #    filename = '~/.config/qtile/Assets/5.png',                
                #),  

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/1.png',                
                #    background = '#52548D',
                #),

                widget.CPU(
                    font = "UNDERWAVE",
                    format='CPU:({load_percent:.1f}%/{freq_current}GHz)',
                    fontsize = 13,
                    foreground='#E0D5FF',
                    margin = 0,
                    padding = 0,
                    background = '#4A2D7A',
                    mouse_callbacks = {'Button1': open_btop},
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background = '#52548D',
                ),  
  
                widget.Systray(
                    background = '#4A2D7A',
                    icon_size = 20,
                    padding = 6,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/5.png',
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/2.png',                
                    background = '#52548D',
                ),                    
                                                
               
                widget.Memory(
                    format='RAM: ({MemUsed:.1f}GB/{MemTotal:.1f}GB | {MemPercent:.0f}%)',
                    measure_mem='G',           # use gigabytes
                    font="UNDERWAVE",
                    foreground='#E0D5FF',
                    fontsize=13,
                    padding=8,
                    background='#4A2D7A',
                    mouse_callbacks={'Button1': open_btop},
                ),


                widget.Spacer(
                    length = 6,
                    background = '#4A2D7A',
                ),  

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/volume.svg',
                    background = '#4A2D7A',
                    margin_y = 3,
                    scale = True,
                ),

                widget.Spacer(
                    length = 4,
                    background = '#4A2D7A',
                ), 

                widget.PulseVolume(
                    font= 'UNDERWAVE',
                    fontsize = 13,
                    foreground='#E0D5FF',
                    padding = 2,
                    background = '#4A2D7A',
                ),

                widget.Spacer(length=15, background='#4A2D7A'),

                #widget.Image(
                #    filename = '~/.config/qtile/Assets/5.png',
                #),                


                #widget.Image(
                #    filename = '~/.config/qtile/Assets/1.png',                
                #    background = '#4B427E',
                #),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/calendar.svg',
                    background = '#4A2D7A',
                    margin_y = 5,
                    scale = True,
                ),

                widget.Spacer(
                    length = 6,
                    background = '#4A2D7A',
                ), 
        
                widget.Clock( # Calendar
                    format = '%d.%m.%y ', #Here you can change between USA or another timezone
                    background = '#4A2D7A',
                    foreground='#E0D5FF',
                    font = "UNDERWAVE",
                    fontsize = 15,
                    padding = 0,
                ),

                widget.Image(
                    filename = '~/.config/qtile/Assets/Bar-Icons/clock.svg',
                    background = '#4A2D7A',
                    margin_y = 3,
                    margin_x = 5,
                    scale = True,
                ),

                widget.Clock(
                    format = '%H:%M', 
                    background = '#4A2D7A',
                    foreground='#E0D5FF',
                    font = "UNDERWAVE",
                    fontsize = 15,
                    padding = 0,
                ),

                widget.Spacer(
                    length = 18,
                    background = '#4A2D7A',
                ),
            ],
            30,  # Bar size (all axis)
            margin = [0, 0, 5, 0],    # Can also be 0 instead of 5
            # [Top, Right, Bottom, Left]
            border_width = [0, 0, 3, 0],
            border_color = '#7B52C4',
            background = '#180F28',
        ),
        
        wallpaper='~/.config/qtile/Wallpaper/WavyPills.png',
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False #This basically puts your mouse in the center on the screen after you switch to another workspace
floating_layout = layout.Floating(
	border_focus='#C084FC',
	border_normal='#1F1D2E',
	border_width=3,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
from libqtile import hook
# some other imports
import os
import subprocess
# stuff
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh') # path to my script, under my user directory
    subprocess.call([home])

auto_fullscreen = True
focus_on_window_activation = "focus" #or focus
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
