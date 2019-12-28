from django.db import models


class GitHubAddress(models.Model):
    address = models.CharField(max_length=100,
                               null=False,
                               blank=False,
                               db_index=True,
                               unique=True)

    class Meta:
        verbose_name = 'github_commit'
        verbose_name_plural = 'github_commit'

    def __str__(self):
        return "addr: {}".format(self.address)


class GitHubCommit(models.Model):
    created = models.DateField(blank=False)
    modified = models.DateField(blank=True)
    last_commit = models.DateField(blank=True)
    total_commit = models.IntegerField(default=0)
    continuous_commit = models.IntegerField(default=0)
    address = models.ForeignKey('GitHubAddress', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'github_commit'
        verbose_name_plural = 'github_commit'

    def __str__(self):
        return "addr: {} / total commit: {} / continuous commit: {}".format(
            self.address, self.total_commit, self.continuous_commit
        )
