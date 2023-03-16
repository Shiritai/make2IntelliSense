# make2IntelliSense for VSCode C/C++ & Linux kernel development

Python scripts converting makefile into [C/C++ extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) configuration files to make IntelliSense work better, also disable file indexing listed in `.gitignore`.

Inspired by the brutal way introduced in [Stupid Python Tricks: VSCODE c_cpp_properties.json for Linux Kernel Development](https://iotexpert.com/stupid-python-tricks-vscode-c_cpp_properties-json-for-linux-kernel-development/), I modify several parts to make it more useful. Plus a script to keep VSCode out of indexing object files, which the files are usually meaningless for indexing and slow down VSCode. I may keep updating this repository in the future if needed.

Always feel free to modify and give your patch :)

## Requirement

* Linux/macOS environment
* If you're developing linux kernel module, then make sure you have installed a proper linux-header
    * You may use `uname -r` command to check if it exists.
* `make` command
* (optional) A proper `Makefile` file in your target directory for compiling you project
* (optional) A proper `.gitignore` file in your target directory for git

## Usage

1. Clone repository
2. Run make script as

    ```bash
    make TAR_DIR=YOU_TARGET_DIRECTORY
    ```

    For example, if you clone `linux` repository into directory `~/repos/linux`, then you may type:

    ```bash
    make TAR_DIR=~/repos/linux
    ```

Done :), you'll see your customized `c_cpp_properties.json` and `settings.json` files under `.vscode` in you target directory.

## Trouble shooting

If you encounter some dependency issue, that is, if make command invoked by `gen_c_cpp_properties.py` stuck because lost of previous object files, then you can edit `MODE` variable in Makefile to use real make process for `c_cpp_properties.json` generation.

To enable real make process, set `MODE` to empty space like:

```bash
make TAR_DIR=YOU_REPO_DIRECTORY MODE= 
```
For example, if you're again setting linux developing environment, than you can use the following command.

```bash
make TAR_DIR=~/repos/linux MODE= 
```