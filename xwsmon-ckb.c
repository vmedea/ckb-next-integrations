/**
 * Workspace switch monitor for ckb-next. This will highlight the key associated with the current workspace.
 * This needs the "pipe" animation to be configured in the ckb-next GUI.
 *
 * Mara Huldra 2021 :: SPDX-License-Identifier: MIT
 *
 * Based loosely on an example by Ruslan (https://stackoverflow.com/questions/2641766/python-x11-find-out-if-user-switches-virtual-desktops).
 */
#include <X11/Xlib.h>

#include <errno.h>
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

/** Default ckbnext pipe to use. */
#define PIPE_FILE "/tmp/ckbpipe000"

/** Keys to highlight for workspaces. */
const char *default_keys[] = {
    "g1", "g2", "g3", "g4", "g5", "g6"
};

/** Default color for active workspace key (0xRRGGBBAA). */
const uint32_t COLOR_ACTIVE = 0xffffffff;

/** Default color for inactive workspace key (0xRRGGBBAA). */
const uint32_t COLOR_INACTIVE = 0x00000000;

struct AppData {
    /** Filename for pipe. */
    const char *pipe_file;
    /** Number of keys. */
    uint32_t nkeys;
    /** Key names. */
    const char **keys;
    /** Color for active/inactive key. */
    uint32_t color[2];

    /** X11 atom for NET_CURRENT_DESKTOP. */
    Atom atom;
};

/** Highlight the key for the currently active workspace.
 */
static void highlight_current_workspace(struct AppData* appdata, Display *display, Window window)
{
    Atom actualType;
    int actualFormat;
    unsigned long nitems, remainingBytes;
    unsigned char* prop;

    if (XGetWindowProperty(display, window, appdata->atom,
                          0, 1, False, AnyPropertyType,
                          &actualType, &actualFormat, &nitems, &remainingBytes,
                          &prop) != Success)
    {
        fprintf(stderr, "<3>Failed to get current desktop number\n");
        return;
    }

    if(nitems != 1 || remainingBytes != 0 || actualFormat != 32)
    {
        XFree(prop);
        fprintf(stderr, "<3>Unexpected number of items (%lu) or remaining bytes (%lu)"
                        " or format (%d)\n", nitems, remainingBytes, actualFormat);
        return;
    }

    uint32_t value;
    memcpy(&value, prop, sizeof(value));
    XFree(prop);

    fprintf(stderr, "<7>Switch to workspace %d detected\n", value);

    /* Initially, open the pipe as non-blocking, to prevent a stale pipe socket
     * from hanging the process.
     */
    int pipe_fd = open(appdata->pipe_file, O_WRONLY | O_NONBLOCK);
    if (pipe_fd < 0) {
        /* Could not open the pipe, ignore this. */
        fprintf(stderr, "<4>warning: Could not open pipe %s: %s\n", appdata->pipe_file, strerror(errno));
        return;
    }
    /* After connecting set to blocking. */
    if (fcntl(pipe_fd, F_SETFL, 0) < 0) {
        fprintf(stderr, "<4>warning: Could not set pipe to blocking\n");
    }
    fprintf(stderr, "<7>Opened pipe %s succesfully\n", appdata->pipe_file);

    for (int i = 0; i < appdata->nkeys; ++i) {
        dprintf(pipe_fd, "rgb %s:%08x\n", appdata->keys[i], appdata->color[i == value]);
    }
    close(pipe_fd);
}

int main(int argc, char** argv)
{
    struct AppData appdata = {};

    appdata.pipe_file = PIPE_FILE;
    appdata.nkeys = sizeof(default_keys) / sizeof(*default_keys);
    appdata.keys = default_keys;
    appdata.color[0] = COLOR_INACTIVE;
    appdata.color[1] = COLOR_ACTIVE;

    Display *display = XOpenDisplay(NULL);

    if (!display) {
        fprintf(stderr, "<3>Cannot run without an X display\n");
        exit(1);
    }

    Window window = DefaultRootWindow(display);

    appdata.atom = XInternAtom(display, "_NET_CURRENT_DESKTOP", True);

    XSelectInput(display, window, PropertyChangeMask);

    highlight_current_workspace(&appdata, display, window);

    while (1) {
        XEvent event;
        XNextEvent(display, &event);

        switch (event.type) {
        case PropertyNotify: {
            const XPropertyEvent* const prop_evt = (const XPropertyEvent*)&event;
            if(prop_evt->state != PropertyNewValue || prop_evt->atom != appdata.atom)
                break;

            highlight_current_workspace(&appdata, display, window);
        } break;
        default:
            break;
        }
    }

    return 0;
}
