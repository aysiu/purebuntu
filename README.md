# purebuntu
Generates apt-get commands to remove *buntu-desktop metapackages and dependencies from other *buntu-desktop metapackages

## What is this for?
On [Ubuntu](https://ubuntu.com), there are metapackages (basically pointers or umbrellas) that point to or include a bunch of other software packages. So if you install _kubuntu-desktop_, _kubuntu-desktop_ itself is a tiny "package" that just brings in a lot of other packages. Unfortunately, removing the metapackage later does not remove all the packages that were brought in originally.

## Why script it?
Well, I was [doing this manually](http://www.psychocats.net/ubuntucat/tag/pure-ubuntu/) for many years, and it honestly gets tiresome, so I figured I'd just script it to make it somewhat future-proof.

## How do I use the script?
* Download the [**purebuntu.py**](https://github.com/aysiu/purebuntu/blob/master/purebuntu.py) file from this GitHub repository.
* If you haven't updated your apt cache lately, make sure to run `sudo apt-get update`
* Run the **pureubuntu.py** file using this syntax: `python ~/Downloads/purebuntu.py --remove kubuntu-desktop --keep ubuntu-desktop` but substitute in the metapackages you actually want to keep and remove.
* Take the resulting output and copy and paste it into the terminal

## What metapackages would you use purebuntu for?
* ubuntu-desktop
* kubuntu-desktop
* lubuntu-desktop
* edubuntu-desktop

There may be others, too.

## Why not just run the command instead of generating output to copy and paste?
The commands purebuntu generates involve removing a lot of packages. It's important the user actually consent to those packages being removed. If the list is generated, it gives the option for users to omit some of the packages and still get roughly the same effect as removing the entire set of dependencies from the metapackage (minus those one or two packages they want to keep).

## Are you considering pull requests?
Heck, yes! This is definitely just a first iteration. If people have ways to make this more efficient or useful, I'm open to seeing how purebuntu can improve. If I don't like your suggestions, this is GPL'ed software, so you can fork it and make your own version. Go, open source!
