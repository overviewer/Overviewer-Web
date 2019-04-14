#!/bin/bash
rpm --addsign \
--define "_gpg_name $CODESIGN_NAME" \
--define "__gpg_check_password_cmd /bin/true" \
--define "__gpg_sign_cmd %{__gpg} gpg --batch --no-verbose --no-armor --use-agent -u %{_gpg_name} --no-secmem-warning -sbo %{__signature_filename} %{__plaintext_filename}" \
$1
