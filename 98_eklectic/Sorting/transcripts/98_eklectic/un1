./ct-ng clean
./ct-ng build 2>&1 | awk '{print strftime("[%Y-%m-%d %H:%M:%S]"), $0; fflush()}' | tee haswell-toolchain-build.log
