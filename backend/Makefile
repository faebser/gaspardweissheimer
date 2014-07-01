
.PHONY: all

dev-js:
	$(shell rm -rf website/js)
	$(shell ln -s ../../js website/)

cat-test:
	$(info $(TEST))
	$(shell envsubst < "test" > "test-finished")
