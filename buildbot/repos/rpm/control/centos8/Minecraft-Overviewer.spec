Summary: Generates large resolution images of a Minecraft map.
Name: Minecraft-Overviewer
Version: {VERSION}
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GNU General Public License v3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Vendor: Andrew Brown <brownan@gmail.com>
Url: https://overviewer.org/
Requires: python3-pillow python3-numpy
BuildRequires: wget python36-devel python3-numpy

%description
The Minecraft Overviewer is a command-line tool for rendering high-resolution
maps of Minecraft worlds. It generates a set of static html and image files and
uses the Leaflet javascript library to display a nice interactive map.

%prep
wget -P %{_tmppath} https://github.com/python-pillow/Pillow/archive/5.1.0.tar.gz
tar -xf %{_tmppath}/5.1.0.tar.gz --directory %{_tmppath}
%setup -n %{name}

%build
env CFLAGS="$RPM_OPT_FLAGS" PIL_INCLUDE_DIR=%{_tmppath}/Pillow-5.1.0/src/libImaging %{__python3} setup.py build

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
