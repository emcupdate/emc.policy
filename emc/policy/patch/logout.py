
def logout(self, REQUEST):
    """Publicly accessible method to log out a user
    """
    self.resetCredentials(REQUEST, REQUEST['RESPONSE'])

    # Little bit of a hack: Issuing a redirect to the same place
    # where the user was so that in the second request the now-destroyed
    # credentials can be acted upon to e.g. go back to the login page
    referrer = REQUEST.get('HTTP_REFERER') # optional header
    #referrer = "192.168.0.5/v4/public/index.php?action=logout"
    if referrer:
        REQUEST['RESPONSE'].redirect(referrer)