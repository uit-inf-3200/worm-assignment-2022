#!/usr/bin/env python3

import example_module
import pkg_resources

if __name__ == '__main__':
    print("Hello, World!")
    print(example_module.MODULE_STRING)
    print(pkg_resources \
            .resource_string("resources", "example_resource.txt") \
            .decode("utf-8"))
