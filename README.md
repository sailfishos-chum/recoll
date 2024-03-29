## Recoll for Sailfish OS

For information about what Recoll does, see its [Home Page](https://www.lesbonscomptes.com/recoll/pages/index-recoll.html)

Before starting to index and search, you should probably also take a look at
the [Documentation](https://www.lesbonscomptes.com/recoll/pages/documentation.html).

### Indexer

The package ships a user systemd service and timer for per-user index creation
and updating.

To enable scheduled indexing, do as user:

    systemctl --user enable recollindexuled.timer
    systemctl --user start recollindex.timer

The timer is configured to run twice a day at six, and one hour after a reboot.

To just run the indexer once or whenerver needed, do

    systemctl --user start recollindex.service

At first run, that will create necessary configuration directories at
`~/.recoll`. The default config has been tuned a bit for Sailfish OS, and you
should review `~/.recoll/recoll.conf` and adjust to your needs.

You should primarily make the decision whether to index things like `~/.qmf`
where parts of emails are stored, or `~/android_support`, where user data of
Android Support is kept.

