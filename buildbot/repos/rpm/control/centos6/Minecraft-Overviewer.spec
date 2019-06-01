Summary: Generates large resolution images of a Minecraft map.
Name: Minecraft-Overviewer
Version: {VERSION}
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GNU General Public License v3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Vendor: Andrew Brown <brownan@gmail.com>
Url: http://overviewer.org/
Requires: epel-release python3-pillow python34-numpy
BuildRequires: epel-release git python34-devel python34-numpy

%description
The Minecraft Overviewer is a command-line tool for rendering high-resolution
maps of Minecraft worlds. It generates a set of static html and image files and
uses the Google Maps API to display a nice interactive map.

%prep
git clone https://github.com/python-pillow/Pillow.git %{_tmppath}/Pillow
%setup -n %{name}

%build
env CFLAGS="$RPM_OPT_FLAGS" PIL_INCLUDE_DIR=%{_tmppath}/Pillow/src/libImaging %{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --root=%{buildroot}
rm -rf %{buildroot}%{_defaultdocdir}/minecraft-overviewer

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitearch}/Minecraft_Overviewer-*-*.egg-info
%{python3_sitearch}/overviewer_core
%{_bindir}/overviewer.py
%doc README.rst COPYING.txt sample_config.py
