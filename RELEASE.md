# Release

```bash
bump2version release --tag --verbose
bump2version patch --verbose
git push upstream master --tags
```

## Some extra info on deleting tags!

### Delete remote tag

```shell
git push --delete origin tagname
```

### Delete local tag

```shell
git tag --delete <tagname>
```
