Summary:	Minimalistic, text based, status bar
Name:		xmobar
Version:	0.16
Release:	0.1
License:	BSD
Group:		X11/Window Managers
Source0:	http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4742f1556a8e9b292f18df1176dcd378
URL:		http://projects.haskell.org/xmobar/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-parsec >= 3.1
BuildRequires:	ghc-stm >= 2.3
BuildRequires:	ghc-utf8-string
BuildRequires:	ghc-X11 >= 1.6
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-mtl >= 2.0
Requires:	ghc-parsec >= 3.1
Requires:	ghc-stm >= 2.3
Requires:	ghc-utf8-string
Requires:	ghc-X11 >= 1.6
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
%attr(755,root,root) %{_bindir}/xmobar

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
