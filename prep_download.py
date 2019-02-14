import os
import basis_set_exchange as bse


# Create download files for all formats
dl_dir = os.path.realpath(os.environ.get('BSE_DOWNLOAD_DIR', 'downloads'))
dl_dir_ver = os.path.join(dl_dir, bse.version())
os.makedirs(dl_dir_ver, exist_ok=True)


formats = bse.get_formats()
for fmt in formats:
    base = 'basis_sets-' + fmt + '-' + bse.version()
    for ext in ['.zip', '.tar.bz2']:
        fname = base + ext
        fpath = os.path.join(dl_dir_ver, fname)

        if not os.path.isfile(fpath):
            print('Creating bundle ' + fpath)
            bse.create_bundle(fpath, fmt, 'bib')
