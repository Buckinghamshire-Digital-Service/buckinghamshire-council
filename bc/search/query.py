from django.db.models.fields import CharField
from django.db.models.lookups import PatternLookup


@CharField.register_lookup
class WithinStart(PatternLookup):
    """
    Runs the SQL "<rhs> like <lhs>||'%'"

    This will return matches where the lhs is within the start of the rhs.

    Example:
    `field__withinstart='these'`
    Matches the following values in field:
    ['t', 'th', 'the', 'thes', 'these']

    This is particularly useful for Wagtail Paths as it will return all
    ancestors (inclusive) while using Subquery of Prefetch
    """

    lookup_name = "withinstart"
    param_pattern = "%s||'%%%%'"

    def as_sql(self, compiler, connection):
        field_sql, params = self.process_lhs(compiler, connection)
        path_sql, path_params = self.process_rhs(compiler, connection)
        params.extend(path_params)
        path_lookup = self.param_pattern % field_sql
        rhs_sql = connection.operators["contains"] % path_lookup
        lhs_sql = path_sql
        return "{} {}".format(lhs_sql, rhs_sql), params
