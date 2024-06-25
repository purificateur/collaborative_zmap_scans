**Jupyter Lab Server:** http://localhost:8888/?token=25a3c409b647d628191a992671e24e8612cdb6b2ae3d679b

**Tunnel Jupyter Lab:** `ssh -N researchproject@naxos.ewi.tudelft.nl -J fackkollu@student-linux.tudelft.nl -L 8888:localhost:8888`

**Tunnel Clickhouse Database Naxos:** `ssh -N -L 9000:akropolis.ewi.tudelft.nl:9000 researchproject@naxos.ewi.tudelft.nl -J fackkollu@student-linux.tudelft.nl`

**Tunnel Clickhouse Database Zeus:** `ssh -N -L 9000:akropolis.ewi.tudelft.nl:9000 researchproject@zeus.ewi.tudelft.nl -J fackkollu@student-linux.tudelft.nl`
