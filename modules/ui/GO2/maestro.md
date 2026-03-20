# maestro.md - Contenido de: /home/daniel/tron/programas/TR/modules/ui/GO2

**Extensiones procesadas:** `.sh`

## /home/daniel/tron/programas/TR/modules/ui/GO2/ares-user.sh

```
#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
./ares_ui -mode user -config config.yaml

```

## /home/daniel/tron/programas/TR/modules/ui/GO2/ares-footer.sh

```
#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
./ares_ui -mode footer -config config.yaml

```

## /home/daniel/tron/programas/TR/modules/ui/GO2/ares-anim.sh

```
#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
./ares_ui -mode anim -config config.yaml

```

## /home/daniel/tron/programas/TR/modules/ui/GO2/ares-identity.sh

```
#!/bin/bash
cd /home/daniel/tron/programas/TR/modules/ui/GO2/
./ares_ui -mode avatar -config config.yaml
if [[ "$*" == *"--spinner"* ]]; then
    if [[ "$*" == *"--rotate"* ]]; then
        ./ares_ui -mode spinner -rotate -config config.yaml
    else
        ./ares_ui -mode spinner -config config.yaml
    fi
fi

```

