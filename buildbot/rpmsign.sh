#!/usr/bin/expect -f
# https://ask.fedoraproject.org/en/question/56107/can-gpg-agent-be-used-when-signing-rpm-packages/
spawn rpm --addsign --define "_gpg_name overviewer.org" --define "__gpg_check_password_cmd /bin/true" --define "__gpg_sign_cmd %{__gpg} gpg --batch --no-verbose --no-armor --use-agent -u %{_gpg_name} --no-secmem-warning -sbo %{__signature_filename} %{__plaintext_filename}" {*}$argv
expect -exact "Enter pass phrase: "
send -- "blank\r"
expect eof
