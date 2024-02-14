# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.32
# 

Name:       recoll

# >> macros
# << macros

Summary:    finds documents based on their contents as well as their file names
Version:    1.37.4
Release:    0
Group:      Applications/File
License:    GPLv2+
URL:        https://www.lesbonscomptes.com/recoll
Source0:    %{name}-%{version}.tar.gz
Source1:    recollindex-scheduled.service
Source2:    recollindex-scheduled.timer
Source3:    recoll.conf
Source100:  recoll.yaml
Patch0:     fix-conf-typo.patch
Patch1:     fix-statx-defined.patch
Requires:   aspell-en
Requires:   xdg-utils
Requires(pre): systemd
Requires(preun): systemd
Requires(post): systemd
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(aspell)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xapian-core)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  make
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  gettext
BuildRequires:  gettext-devel

%description
Recoll is a desktop search tool that provides full text search (from
single-word to arbitrarily complex boolean searches)

%if "%{?vendor}" == "chum"
Title: Recoll CLI
DeveloperName: Les bons comptes
PackagedBy: nephros
Type: console-application
Categories:
  - System
  - Utility
PackageIcon: https://www.lesbonscomptes.com/recoll/pics/recoll64.png
Links:
  Homepage: %{url}
  Help: https://www.lesbonscomptes.com/recoll/pages/documentation.html
  Donation: https://www.lesbonscomptes.com/donations/index.html
%endif


%package helpers
Summary:    Package to install runtime helpers for %{name}
Group:      Applications
Requires:   %{name} = %{version}-%{release}
Requires:   poppler-utils
Requires:   libxslt
Requires:   unzip
Requires:   djvulibre

%description helpers
%{summary}.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%{summary}.

%package python
Summary:    Python interface for %{name}
Group:      Applications
Requires:   %{name} = %{version}-%{release}

%description python
%{summary}.

%prep
%setup -q -n %{name}-%{version}/upstream

# fix-conf-typo.patch
%patch0 -p1
# fix-statx-defined.patch
%patch1 -p1
# >> setup
# << setup

%build
# >> build pre
pushd src
# see autogen.sh
cp ylwrap ylwrap.copy
aclocal
libtoolize --copy
automake --add-missing --force-missing --copy
autoconf ||: # this errors out
cp ylwrap.copy ylwrap
# << build pre

%configure --disable-static \
    --with-systemd \
    --with-system-unit-dir=%{_unitdir} \
    --with-user-unit-dir=%{_userunitdir} \
    --disable-webkit \
    --disable-webengine \
    --disable-qtgui \
    --disable-x11mon \
    --disable-userdoc \
    --disable-python-chm \
    --without-fam \
    --enable-recollq

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
pushd src
# << install pre
%make_install

# >> install post
# don't package docs
rm -rf %{buildroot}%{_mandir}

# fix shebangs for python3:
find %{buildroot}%{python3_sitearch} -type f -exec sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +
find %{buildroot}%{_datadir}/%{name}/filters -type f -exec sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

# remove default systemd services:
rm -f %{buildroot}%{_unitdir}/recollindex@.service
rm -f %{buildroot}%{_userunitdir}/recollindex.service
# install custom systemd services:
install -m 0644 -D %SOURCE1 %{buildroot}%{_userunitdir}/recollindex.service
install -m 0644 -D %SOURCE2 %{buildroot}%{_userunitdir}/recollindex.timer

# custom default config
install -m 0644 %SOURCE3 %{buildroot}%{_datadir}/%{name}/examples/recoll.conf.sfos
# << install post

%preun
# >> preun
%systemd_user_preun recollindex.service
%systemd_user_preun recollindex.timer
# << preun

%post
/sbin/ldconfig
# >> post
%systemd_user_post recollindex.service
%systemd_user_post recollindex.timer
# << post

%postun
/sbin/ldconfig
# >> postun
%systemd_user_postun recollindex.service
%systemd_user_postun recollindex.timer
# << postun

%files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{_datadir}/%{name}
%{_userunitdir}/*
%{_datadir}/%{name}/examples/*
%{_libdir}/lib{name}-*.so
# >> files
# << files

%files helpers
%defattr(-,root,root,-)
# >> files helpers
# << files helpers

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}/
# >> files devel
# << files devel

%files python
%defattr(-,root,root,-)
%{_datadir}/%{name}/filters/*
%{python3_sitearch}/*
# >> files python
# << files python
