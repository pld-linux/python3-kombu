#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define 	module	kombu
Summary:	Messaging library for Python
Summary(pl.UTF-8):	Biblioteka komunikatów dla Pythona
Name:		python3-%{module}
Version:	5.0.2
Release:	4
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/kombu/
Source0:	https://files.pythonhosted.org/packages/source/k/kombu/%{module}-%{version}.tar.gz
# Source0-md5:	52192e631ac39a443fb1abeb52299f22
URL:		https://pypi.org/project/kombu/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:20.6.7
%if %{with tests}
BuildRequires:	python3-Pyro4
BuildRequires:	python3-amqp >= 5.0.0
BuildRequires:	python3-amqp < 6.0.0
BuildRequires:	python3-botocore
BuildRequires:	python3-case >= 1.5.2
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.18
%endif
BuildRequires:	python3-pytest
BuildRequires:	python3-pytz
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-amqp
BuildRequires:	python3-sphinx_celery
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQ protocol, and
also provide proven and tested solutions to common messaging problems.

%description -l pl.UTF-8
Celem Kombu jest jak największe ułatwienie wymiany komunikatów w
Pythonie poprzez dostarczenie idomatycznego, wysokopoziomowego
interfejsu do protokołu AMQ oraz sprawdzonych rozwiązań powszechnych
problemów związanych z komunikowaniem.

%package apidocs
Summary:	API documentation for kombu module
Summary(pl.UTF-8):	Dokumentacja API modułu kombu
Group:		Documentation

%description apidocs
API documentation for kombu module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu kombu.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="case.pytest" \
%{__python3} -m pytest t/unit
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS FAQ LICENSE README.rst THANKS TODO
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,reference,userguide,*.html,*.js}
%endif
