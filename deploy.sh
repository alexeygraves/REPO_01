
#!/bin/bash
# Перенос ревизии из ветки dev в prd с установкой тега

# Переход на ветку prd
git checkout prd

# Слияние с веткой dev
git merge dev

# Создание тега для релиза
git tag -a v1.0 -m "Release"

# Отправка изменений и тега в репозиторий
git push origin prd --tags
