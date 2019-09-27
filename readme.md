# Run steps

Run from base directory.

source scripts/setup_paths.sh
- python3 benchmarks/src/generate.py --tier L1 --task example_task --output_path tmp
- python3 benchmarks/src/generate.py --tier L1 --task ExampleTask --output_path tmp --param1 "range(1,10)" --param2 "range(1, 10)"

# Installation Steps

Make a new mbed program for your MCU.

```bash
mbed new <my_name>
cd <my_name>
```

Then we have to add the uTensor library.

```bash
mbed add https://www.github.com/uTensor/uTensor
```

After writing your `main.cpp` file, you can just compile.

```bash
mbed compile -m <boardname> -t GCC_ARM --profile uTensor/build_profile/release.json
```

If it complains about a profile, then try running it without one.

```bash
mbed compile -m <boardname> -t GCC_ARM
```

The official docs for the mbed cli are [here](https://os.mbed.com/docs/mbed-os/v5.13/tools/developing-mbed-cli.html) for reference.
The easiest way to see the correct boardname is by using `mbed detect`.
For example, the NUCLEO F767ZI board has the target `NUCLEO_F767ZI`.


```

## Troubleshooting

### Serialization Error in TF

If the tensorflow stuff gives you an error with serialization:

```
TypeError: __new__() got an unexpected keyword argument 'serialized_options'
```

It may be an issue with the protobuf version. So make sure you have a good protobuf version.

```
pip uninstall protobuf
pip install protobuf
```

and this fixed the issue for me.

### Mac issues with const struct timeval

Sometimes you may get this compiler error:

```
mbed_rtc_time.cpp@111,7: invalid use of incomplete type 'struct timeval'
```

Try installing the toolchain available [here](https://github.com/ARMmbed/mbed-cli-osx-installer/releases/tag/v0.0.10), I think it's an issue with the default compiler installed through brew.

Then, make sure that the cross compiler version is OK.
I think version 6 works the best, rather than version 7.

```bash
brew tap ArmMbed/homebrew-formulae
brew install arm-none-eabi-gcc 
```

If this doesn't install version 6, then try using the official website and downloading the version 6 binary [here](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads).

__Then, make sure that in your `develop.json` or `release.json` that you compile C++ using gnu++11 rather than c++11. This is probably the root cause of the issue, the GNU extensions aren't on by default.__

### Compilation Issues with RELU mismatched templates

If you have an old version of `utensor_cgen` you might get the following error:

```
error: wrong number of template arguments (3, should be 2)
     ctx.push(new ReluOp<uint8_t, float, uint8_t>(),
```

Just update the version of `utensor_cgen`. I went to version 0.3.5.

### Sub not supported operation in uTensor

Make sure you don't use Subtract in Tensorflow when training, and only use Add.
If you use default layers, you might have to implement them from scratch or use a different version of Tensorflow.
