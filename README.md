# Web app to explore bikiDATA

You can use this web ap to explore [bikiDATA](https://github.com/ISE-FIZKarlsruhe/bikidata) files.

To run it, you can use the following command:

```bash
docker run -p 8000:80000 -v $(pwd):/data -e BIKIDATA_DB=/data/bikidata.duckdb ghcr.io/epoz/bikidata-explore:latest
```

If you have a bikidata.duckdb file in the current directory, or otherwise map it into the volume from a different location

Then, you can access the web app at [http://localhost:8000](http://localhost:8000).
