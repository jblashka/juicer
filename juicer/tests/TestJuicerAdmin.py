#!/usr/bin/env python
import unittest
from juicer.admin.JuicerAdmin import JuicerAdmin as ja
from juicer.admin.Parser import Parser as pmoney
from juicer.utils import mute, get_login_info, get_environments


class TestJuicerAdmin(unittest.TestCase):

    def __init(self):
        (self.connectors, self._defaults) = get_login_info()
        for env in get_environments():
            # remove user
            users = self.connectors[env].get('/users/')
            for user in users:
                if user['login'] == 'cjesop':
                    self.connectors[env].delete('/users/%s/' % user['id'])
            # remove repo
            self.connectors[env].delete('/repositories/test-repo-456/')

        super(__init__)

    def setUp(self):
        self.parser = pmoney()
        (self.connectors, self._defaults) = get_login_info()

    def create_test_user(self):
        args = self.parser.parser.parse_args(("user create cjesop --password cjesop --name 'ColonelJesop' --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        mute()(pulp.create_user)(login=args.login, user_name=args.name, password=args.password, \
                                     envs=args.envs)

    def delete_test_user(self):
        args = self.parser.parser.parse_args(("user delete cjesop --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        mute()(pulp.delete_user)(login=args.login, envs=args.envs)

    def create_test_repo(self):
        args = self.parser.parser.parse_args(("repo create test-repo-456 --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        mute()(pulp.create_repo)(arch=args.arch, repo_name=args.name, envs=args.envs)

    def delete_test_repo(self):
        args = self.parser.parser.parse_args(("repo delete test-repo-456 --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        mute()(pulp.delete_repo)(repo_name=args.name, envs=args.envs)

    def test_show_repo(self):
        self.create_test_repo()
        args = self.parser.parser.parse_args(("repo show test-repo-456  --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.show_repo)(repo_name=args.name, envs=args.envs)
        self.assertTrue(any('test-repo-456' in k for k in output))
        self.delete_test_repo()

    def test_delete_repo(self):
        self.create_test_repo()
        args = self.parser.parser.parse_args(("repo delete test-repo-456 --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.delete_repo)(repo_name=args.name, envs=args.envs)
        self.assertTrue(any('deleted' in k for k in output))

    def test_list_repos(self):
        self.create_test_repo()
        args = self.parser.parser.parse_args(("repo list --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.list_repos)(envs=args.envs)
        self.assertTrue('test-repo-456' in output)
        self.delete_test_repo()

    def test_create_repo(self):
        args = self.parser.parser.parse_args(("repo create test-repo-456 --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.create_repo)(arch=args.arch, repo_name=args.name, envs=args.envs)
        self.assertTrue(any('created' in k for k in output))
        self.delete_test_repo()

    def test_create_user(self):
        args = self.parser.parser.parse_args(("user create cjesop --password cjesop --name 'ColonelJesop' --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.create_user)(login=args.login, user_name=args.name, \
                                                  password=args.password, envs=args.envs)
        self.assertTrue(any((('created' in k) or ('shares' in k)) for k in output))
        self.delete_test_user()

    def test_delete_user(self):
        self.create_test_user()
        args = self.parser.parser.parse_args(("user delete cjesop --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.delete_user)(login=args.login, envs=args.envs)
        self.assertTrue(any('deleted' in k for k in output))

    def test_show_user(self):
        self.create_test_user()
        args = self.parser.parser.parse_args(("user show cjesop --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.show_user)(login=args.login, envs=args.envs)
        self.assertTrue(any('cjesop' in k for k in output))
        self.delete_test_user()

    def test_list_roles(self):
        args = self.parser.parser.parse_args(("role list --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.list_roles)(envs=args.envs)
        self.assertTrue(any('super-users' in k for k in output))

    def test_role_add(self):
        self.create_test_user()
        args = self.parser.parser.parse_args(("role add --login cjesop \
                --role super-users --in %s" % self._defaults['start_in']).split())
        pulp = ja(args)
        output = mute(returns_output=True)(pulp.role_add)(role=args.role, login=args.login, envs=args.envs)
        self.assertTrue(any('added' in k for k in output))
        self.delete_test_user()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestJuicerAdmin)
    unittest.TextTestRunner(verbosity=2).run(suite)
