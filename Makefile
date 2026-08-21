install:
	uv sync

d-build:
	uv build

package-install:
	uv tool install dist/*.whl


package-reinstall: 	d-build
	uv tool install --force dist/*.whl
