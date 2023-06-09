# make2IntelliSense for VSCode C/C++ & Linux kernel development

Python scripts converting makefile into [C/C++ extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) configuration files to make IntelliSense work better, also disable file indexing listed in `.gitignore`.

Inspired by the brutal way introduced in [Stupid Python Tricks: VSCODE c_cpp_properties.json for Linux Kernel Development](https://iotexpert.com/stupid-python-tricks-vscode-c_cpp_properties-json-for-linux-kernel-development/), I modify several parts to make it more useful. Plus a script to keep VSCode out of indexing object files, which the files are usually meaningless for indexing and slow down VSCode. I may keep updating this repository in the future if needed.

In current version, I customize some properties to better fit your machine, the following properties will be auto detected.

* include path of...
    * workspace folder
    * linux kernel header
    * compiler library
* macro defines, including
    * normal define
    * macros with value
* compiler path
* language standard

Always feel free to modify and give your patch :)

## Requirement

* Linux environment
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

To remove generated configuration files, use `make clean` (of course you can add `TAR_DIR` parameter).

## Trouble shooting

### About file exclusion and `.gitignore`

If you don't have `.gitignore` file, you can also run the script to generate `settings.json`. There are two options about file exclusion, `COPY_GIT_IGNORE` and `USE_GIT_IGNORE`. The following table shows their difference.

|option|method|default|
|:-:|:-:|:-:|
|`COPY_GIT_IGNORE`|Set excluding files by copy ignored filenames according to `.gitignore` (it's ok if `.gitignore not exist`) with default ignorant and specified-file bypassing|V|
|`USE_GIT_IGNORE`|Set excluding files by VSCode `explorer.excludeGitIgnore` option||

For `COPY_GIT_IGNORE` case, I introduce two more parameters in `gen_file_exclude.py`: `replace` for replacing some glob pattern into what we specified and `bypass` to skip excluding some files. For now, I replace `.*` glob pattern into `.[^v]*` and bypass `.vscode` not to hide `.vscode` directory, which is a bit unnatural for a VSCode user.

For example, if you want to exclude files following `.gitignore`, you can

```bash
make OPT=USE_GIT_IGNORE
```

such as

```bash
make TAR_DIR=~/repos/linux OPT=USE_GIT_IGNORE
```

Notice that in this case, the result will accidentally be the same since linux ignores all `.*` files and I haven't figure out a better way to bypass some `.*` files. If you have any idea, please contact my :)

### Make dependency issue

If you encounter some dependency issue, that is, if make command invoked by `gen_c_cpp_properties.py` stuck because lost of previous object files, then you can edit `MODE` variable in Makefile to use real make process for `c_cpp_properties.json` generation.

To enable real make process, set `MODE` to empty space like:

```bash
make TAR_DIR=YOU_REPO_DIRECTORY MODE= 
```
For example, if you're again setting linux developing environment, than you can use the following command.

```bash
make TAR_DIR=~/repos/linux MODE= 
```

### Fail to parse after make

If you've run `make` inside target directory before running `make` of this repo's, you may sometimes got a wrong result since files are all made, so there will be no more making output to catch and parse. In this case, you can first `make clean` inside target directory, then run `make` in this repo again.