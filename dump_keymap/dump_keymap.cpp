/**
 * Dump key map from ckb-next in a Python-friendly format.
 *
 * Mara Huldra 2021
 * SPDX-License-Identifier: MIT
 */
#include <QMap>

#include <iostream>
#include <limits>
#include <string>
#include <tuple>
#include <vector>

#include "keymap.h"

int main() {
    KeyMap key_map(KeyMap::Model::K95P, KeyMap::Layout::US);
    QHash<QString, Key> map = key_map.map();
    QHash<QString, Key>::const_iterator i;
    std::vector<std::tuple<std::string, int, int, std::string>> key_list;
    for (i = map.constBegin(); i != map.constEnd(); ++i) {
        if (i->hasLed) {
            std::string friendly_name = i->friendlyName().toStdString();
            for (char &ch: friendly_name) {
                if (ch == '\n') ch = ' ';
            }
            key_list.push_back(std::make_tuple(i.key().toStdString(), i->x, i->y, friendly_name));
        }
    }

    std::sort(key_list.begin(), key_list.end(), [](auto& a, auto& b) {
        if (std::get<2>(a) < std::get<2>(b)) { // Sort by y first...
            return true;
        } else if (std::get<2>(a) > std::get<2>(b)) {
            return false;
        }
        return std::get<1>(a) < std::get<1>(b); // Then x
    });

    int prevy = std::numeric_limits<int>::min();
    for (auto& [name, x, y, friendly_name]: key_list) {
        if (prevy != std::numeric_limits<int>::min() && prevy != y) std::cout << std::endl;
        std::cout << "'" << name << "'" << ": (" << x << ", " << y << "), # " << friendly_name << std::endl;
        prevy = y;
    }

    return 0;
}
