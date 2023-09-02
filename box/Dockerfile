FROM python:3.11-slim-buster

ENV LANG C.UTF-8

COPY packages /etc/packages
COPY odoo16-requirements.txt /etc/
COPY python3-requirements.txt /etc/

RUN apt-get update && apt-get install -y libpq-dev

RUN set -x; \
        apt-get update && \
        DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
# necessary base packages for odoo
            ca-certificates \
            curl \
            git wget \
            gnupg2 \
            python3-dev \
            python3-pip \
            python3-renderpm \
            python3-setuptools \
            python3-wheel \
            python3-watchdog \
            libssl-dev \
            libjpeg62-turbo \
            multiarch-support \
            xz-utils \
            gcc \
            bzr zip unzip \       
            pysassc \
            libfontconfig1 libxrender1 libxext6 \
            fontconfig xfonts-75dpi xfonts-base \
            build-essential libldap2-dev libsasl2-dev ldap-utils \
            locales; \
# necessary packages for wkhtmltopdf
            dpkg -i /etc/packages/*.deb && \
            rm -r /etc/packages/; \
# install nodejs
            apt-get install -y curl && \
            curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
            apt-get install -y nodejs && \
            npm install -g postcss rtlcss less less-plugin-clean-css; \
# setting locale
            sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen; \
# install postgresql
            echo 'deb http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main' > /etc/apt/sources.list.d/pgdg.list && \
            GNUPGHOME="$(mktemp -d)" && \ 
            export GNUPGHOME && \ 
            repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' && \ 
            apt-get install -y gnupg && \
            gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" && \ 
            gpg --batch --armor --export "${repokey}" > /etc/apt/trusted.gpg.d/pgdg.gpg.asc && \ 
            gpgconf --kill all && \ 
            rm -rf "$GNUPGHOME" && \ 
            apt-get update && \ 
            apt-get install --no-install-recommends -y postgresql-client && \ 
            rm -f /etc/apt/sources.list.d/pgdg.list && \ 
            rm -rf /var/lib/apt/lists/*; \   
# install python3 libs 
            pip3 install --no-cache-dir --upgrade pip && \
            pip3 install --no-cache-dir --upgrade redis && \
            pip3 install --no-cache-dir -r /etc/odoo16-requirements.txt && \
            pip3 install --no-cache-dir -r /etc/python3-requirements.txt; \
# clean apt cache
            apt-get autoremove -y && \
            apt-get clean

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
