
Required Packages:

Beautifulsoup4, python library: tarball is in the folder.
$ sudo pip install beautifulsoup4

Nltk, python library
$ sudo pip install -U nltk

Nltk data sets
$ sudo python -m nltk.downloader -d /usr/share/nltk_data all

Python source code should be in the same directory with the input files. (reuter files)
No need for stopwords.txt, i am using stopwords from ntlk library.

After that:

$ python assignment1.py

It creates inverted_index and asks some questions related to user's query.
Then gives the output of search in the form of indexes.
