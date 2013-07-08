# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo 'Provisioning Exitwp Library Dependencies...'
apt-get update --fix-missing
apt-get install -q -y git python-pip
apt-get install -q -y python-yaml python-bs4 python-html2text libyaml-dev python-dev
cd /vagrant
echo 'Provisioning Exitwp Python Requirements...'
pip install --upgrade -r pip_requirements.txt
echo 'Provisioning complete!'
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "Puppetlabs Ubuntu 12.04.2 x86_64, VBox 4.2.10, No Puppet or Chef"
  config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/ubuntu-server-12042-x64-vbox4210-nocm.box"
  config.vm.provision :shell, :inline => $script
end