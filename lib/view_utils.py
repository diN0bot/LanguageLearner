from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
import settings
from json_utils import json_response

def render_response(request, template, dictionary=None):
    """
    Return render_to_response with
    context_instance=RequestContext(request).
    """
    dictionary = dictionary or {}
    #if 'request' in dictionary:
    #    del dictionary['request']
    return render_to_response(template, dictionary, context_instance=RequestContext(request))

def render_string(request, template, dictionary=None):
    dictionary = dictionary or {}
    return render_to_string(template, dictionary, context_instance=RequestContext(request))

def superuser(user):
    return user and user.is_authenticated() and user.is_superuser

def staff(user):
    return user and user.is_authenticated() and user.is_staff

def logged_in(user):
    return user and user.is_authenticated()

def session(session_key):
    return request.session.get(session_key, False)

def user_criteria(crit_func):
    """
    Decorator for views. Expects a user_criteria function, eg superuser, staff, logged_in.
    If current user meets criteria, view is called; otherwise, redirect to login.
    """
    def decorator(fn):
        def inner(*iargs, **kwargs):
            #user = current_user()
            #if reduce(lambda x,y: x(user) and y(user), args):
            if crit_func(iargs[0].user):
                # user passes all user criteria
                return fn(*iargs, **kwargs)
            else:
                return HttpResponseRedirect('%s?redirect_to=%s' % (reverse('login'), iargs[0].path))
        return inner
    return decorator

def ajax(crit_fun1, crit_fun2=None):
    """
    Decorator for views accessed via ajax. Expects a user_criteria function, 
    eg superuser, staff, logged_in. If criteria function fails, returns json error.
    """
    def decorator(fn):
        def inner(*iargs, **kwargs):
            if crit_fun1(current_user()):
                return fn(*iargs, **kwargs)
            if crit_fun2 and crit_fun2(current_user()):
                return fn(*iargs, **kwargs)
            # user passes no criteria
            return json_response('Could not perform action: user fails to meet criteria')
        return inner
    return decorator
  
def extract_parameters(request, method_type, expected_parameters, optional_parameters=None, debug=False):
  """
  Convenience utility for extracting URL parameters
  @param request:
  @param method_type: "GET" or "POST"
  @param expected_parameters: list of required parameter names
  @param optional_parameters: list of optional parameter items. Items may be string names or (name, default value) tuples.
      eg: ["offset", "range"] or ["offset", ("range", 20)]
      If the item is not present in the request, then:
         If no default is provided, the item is absent from the returned parameters dict
         If a default is provided, the item with default value is present in the returned parameters dict
  @param debug: If True, explicit failure reasons are returned. If False, vague failure reasons are alluded to.
  """
  DOCS_URL = "https://projects.cloudkick.com/projects/ck/wiki/GraphBrowserAPI"
  ERROR_MSG = "Something unexpected happened"
  
  ret = {}

  if not getattr(request, method_type) and expected_parameters:
    return {'success': False,
            'reason': "Expected %s parameters. See %s" % (method_type, DOCS_URL)}
  
  for p in expected_parameters:
    try:
      v = getattr(request, method_type).get(p, None)
      if v == None:
        return {'success': False,
                        'reason': "Missing expected parameter: %s. See %s" % (p, DOCS_URL)}
      ret[p] = v
    except:
      reason = debug and "Something unexpected happened while extracting parameters from URL" or ERROR_MSG
      return {'success': False,
              'reason': reason}
    
  optional_parameters = optional_parameters or {}
  for p in optional_parameters:
    if isinstance(p, (tuple,list)):
      name = p[0]
      default = p[1]
    else:
      name = p
      default = None
    try:
      v = getattr(request, method_type).get(name, default)
      # v might be v by default
      if v or isinstance(p, (tuple,list)): 
        ret[name] = v or default
    except:
      reason = debug and "Something unexpected happened while extracting optional parameters from URL" or ERROR_MSG
      return {'success': False,
              'reason': reason}
     
    
  return {'success': True,
          'parameters': ret}
  