from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_tables2 import RequestConfig
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from models import *
#from tables import HoldingsTable, TransactionsTable
#from forms import CreateEditTransactionForm, HoldingForm

#class HoldingCreate(CreateView):
#    model = Holding
#    form_class = HoldingForm

#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(HoldingCreate, self).dispatch(*args, **kwargs)

#    def form_valid(self, form):
#        form.instance.user = self.request.user
#        return super(HoldingCreate, self).form_valid(form)

#class HoldingUpdate(UpdateView):
#    model = Holding

#class HoldingDelete(DeleteView):
#    model = Holding

#def HoldingList(request):
#    form = CreateEditTransactionForm()

#    holdings = Holding.objects.all()
#    table = HoldingsTable(holdings)
#    RequestConfig(request).configure(table)

#    return render_to_response('portfolio/holding_list.html',
#                              {'holding_list': holdings,
#                               'table': table,
#                               'form': form},
#                               context_instance=RequestContext(request))

#def HoldingDetail(request, id):
#    holding = Holding.objects.get(pk=id)
#    transactions = Transaction.objects.filter(Q(to_holding__id=id) | Q(from_holding__id=id))
#    transaction_table = TransactionsTable(transactions)
#    RequestConfig(request).configure(transaction_table)
#    return render_to_response('portfolio/holding_detail.html',
#                              {'holding': holding,
#                               'transactions': transactions,
#                               'transaction_table': transaction_table},
#                               context_instance=RequestContext(request))

#def holding_delete(request, id):
#    holding = Holding.objects.get(pk=id)
#    if request.POST.get('delete'):
#        holding.delete()
#        return redirect(reverse('holdings_list'))
#    else:
#        return redirect(holding.get_absolute_url())
