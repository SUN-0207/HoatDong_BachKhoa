# Use the novobidevops/odoo:15 image as the base image
FROM novobidevops/odoo:15
# FROM novobidevops/odoo-arm:15


# Install additional packages
RUN apt-get update && \
    pip3 install html2text==2020.1.16 vietnam-provinces python-docx reportlab && \
    pip3 install SkPy==0.10.4 && \
    pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client; \
    apt-get autoremove -y && \
    apt-get clean
