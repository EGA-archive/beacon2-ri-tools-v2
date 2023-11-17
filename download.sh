wget https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2
curl -L https://snpeff.blob.core.windows.net/versions/snpEff_latest_core.zip > snpEff_latest_core.zip
unzip snpEff_latest_core.zip

wget https://github.com/samtools/bcftools/releases/download/1.15.1/bcftools-1.15.1.tar.bz2 -O bcftools.tar.bz2
tar -xjvf bcftools.tar.bz2
cd bcftools-{version}
make
sudo make prefix=/usr/local/bin install
sudo ln -s /usr/local/bin/bin/bcftools /usr/bin/bcftools