#!/usr/bin/env python2.7

import apt
import os


class SourcePackageFilter(apt.cache.Filter):
    def __init__(self, source_packages):
        self.spkgs = source_packages

    def apply(self, pkg):
        if pkg.is_installed:
            if pkg.installed.source_name in self.spkgs:
                return True
        return False


class KernelCleaner(object):
    def __init__(self):
        self.c = apt.cache.Cache()

    def get_kernels(self):
        return self.c.get_providing_packages("linux-image")

    def get_tracks(self):
        return set([(pkg.installed or pkg.candidate).source_name for pkg in self.get_kernels()])

    def get_packages(self):
        packages = apt.cache.FilteredCache(self.c)
        packages.set_filter(SourcePackageFilter(self.get_tracks()))
        return packages

    def mark_kernels_auto(self):
        for pkg in self.get_packages():
            pkg.mark_auto()
        self.c.commit()

    def purge_old_kernels(self):
        release = os.uname()[2]
        for pkg in self.get_packages():
            if release not in pkg.name:
                if pkg.is_auto_removable:
                    pkg.mark_delete(auto_fix=False, purge=True)
        self.c.commit()


def main():
    kc = KernelCleaner()
    kc.mark_kernels_auto()
    kc.purge_old_kernels()


if __name__ == "__main__":
    main()
