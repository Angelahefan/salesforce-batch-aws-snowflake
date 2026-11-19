def reconcile(results):
 failed=[r for r in results if r['rows'] < 0]
 if failed: raise RuntimeError(f'CDC reconciliation failed: {failed}')
 return {'status':'passed','objects':len(results),'rows':sum(r['rows'] for r in results)}
