make:
	rm -rf indico_hub/*
	cp -r ../../indico-hub/indico_hub/* indico_hub
push:
	echo "enter commit message"
	read MSG
	git add .
	git -m $${MSG}
	git push
