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
