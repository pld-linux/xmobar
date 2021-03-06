# Conditional build:
%bcond_without	alsa		# don't use alsa
%bcond_without	datezone	# don't use datezone
%bcond_without	dbus		# don't use dbus
%bcond_without	inotify		# don't use inotify
%bcond_without	mpd		# don't use mpd
%bcond_without	xft		# don't use xft
#
Summary:	Minimalistic, text based, status bar
Name:		xmobar
Version:	0.24.3
Release:	2
License:	BSD
Group:		X11/Window Managers
Source0:	http://hackage.haskell.org/packages/archive/xmobar/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8d0b8e12da0346ab74b113b83bed11d0
URL:		http://projects.haskell.org/xmobar/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-X11 >= 1.6
%{?with_xft:BuildRequires:	ghc-X11-xft >= 0.2}
%{?with_alsa:BuildRequires:	ghc-alsa-core >= 0.5}
%{?with_alsa:BuildRequires:	ghc-alsa-mixer >= 0.2.0.3}
%{?with_dbus:BuildRequires:	ghc-dbus >= 0.10}
%{?with_inotify:BuildRequires:	ghc-hinotify >= 0.3}
%{?with_mpd:BuildRequires:	ghc-libmpd >= 0.9}
BuildRequires:	ghc-mtl >= 2.2.1
BuildRequires:	ghc-parsec >= 3.1
BuildRequires:	ghc-regex-compat
BuildRequires:	ghc-stm >= 2.3
%{?with_datezone:BuildRequires:	ghc-timezone-olson >= 0.1}
%{?with_datezone:BuildRequires:	ghc-timezone-series >= 0.1}
BuildRequires:	ghc-utf8-string
BuildRequires:	rpmbuild(macros) >= 1.608
BuildRequires:	xorg-lib-libXpm-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
Minimalistic, text based, status bar.

%package doc
Summary:	HTML documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{name}
Group:		Documentation

%description doc
HTML documentation for %{name}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{name}.

%prep
%setup -q

%build
runhaskell Setup.lhs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version} \
	%{?with_alsa:--flags="with_alsa"} \
	%{?with_datezone:--flags="with_datezone"} \
	%{?with_dbus:--flags="with_dbus"} \
	%{?with_inotify:--flags="with_inotify"} \
	%{?with_mpd:--flags="with_mpd"} \
	%{?with_xft:--flags="with_xft"}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc news.md readme.md samples/xmobar.config
%attr(755,root,root) %{_bindir}/xmobar

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
