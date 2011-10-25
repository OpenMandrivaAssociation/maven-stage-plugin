%define project_version 1.0-alpha-2
Name:           maven-stage-plugin
Version:        1.0
Release:        0.2.alpha2
Summary:        Plugin to copy artifacts from one repository to another

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-stage-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-stage-plugin-1.0-alpha-2/
# tar jcf maven-stage-plugin-1.0-alpha-2.tar.bz2 maven-stage-plugin-1.0-alpha-2/
Source0:        %{name}-%{project_version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: plexus-utils
BuildRequires: ant-nodeps
BuildRequires: maven2
BuildRequires: maven-install-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: jpackage-utils
Requires: ant-nodeps
Requires: maven2
Requires: jpackage-utils
Requires: java
Requires(post): jpackage-utils
Requires(postun): jpackage-utils 

Obsoletes: maven2-plugin-stage <= 0:2.0.8
Provides: maven2-plugin-stage = 1:%{version}-%{release}

%description
The Maven Stage Plugin copies artifacts from one repository to another. 
Its main use is for copying artifacts from a staging repository to 
the real repository.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires: jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{project_version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.failure.ignore=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{project_version}.jar   %{buildroot}%{_javadir}/%{name}-%{project_version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{project_version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{project_version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins %{name} %{project_version} JPP %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{project_version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{project_version}/
ln -s %{name}-%{project_version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{project_version}
%{_javadocdir}/%{name}

