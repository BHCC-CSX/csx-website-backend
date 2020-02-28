# Using Git
Git is a command line tool for managing git repositories. However, just because it is a command line
tool does not mean that you have to use it in the command line. There are many GUI Git clients out there
that make working with git very user friendly. 

You can find a list of Git GUI clients on the [GUI Clients page at git-scm.com](https://git-scm.com/downloads/guis).

## Cloning a Repository
Cloning (downloading) a repository (also called a repo), can be done in the command line, by first navigating to the
directory where you want the repository's files to go. Then running the following command.

```bash
$ git clone REPO_URL
```

Where `REPO_URL` is the url of the repository that you wish to clone. Once cloned, you will have an exact copy of
the repository as it was the moment you cloned it.

## Pulling Changes
So, now you have a copy of the repository, but some one has made a change, and you don't see it on
your computer. To get these changes synced to your computer you run the `git pull` command, which is 
like the clone command, except it only downloads the changes that have been made since the last time you pulled (or cloned).

### The Fetch Command
In using GUI clients or googling around, you will likely come across mentions of the `git fetch` command. On
the surface, the fetch command seems to do the same thing that the pull command does. However, they are slightly different.

The fetch command will get information from the remote repository about changes that have happened since the last time you pulled/fetched/cloned
but it will not actually download the changes, so will not affect your working files.

## Making Changes
This is the fun part. We get to write code, and share it with everyone!
