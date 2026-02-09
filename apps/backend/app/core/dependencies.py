from fastapi import Depends, HTTPException, Header
from app.core.supabase import supabase

def get_current_user(authorization: str = Header(...)):
    """取得當前使用者"""
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="無效的 token")

def get_current_org(
    user = Depends(get_current_user),
    org_id: str = Header(None, alias="X-Org-ID")
):
    """取得當前組織"""
    if not org_id:
        # 取得使用者的第一個 org
        result = supabase.table("org_members")\
            .select("org_id")\
            .eq("user_id", user.id)\
            .limit(1)\
            .execute()
        
        if result.data:
            org_id = result.data[0]["org_id"]
        else:
            raise HTTPException(status_code=400, detail="找不到組織")
    
    # 驗證成員資格
    result = supabase.table("org_members")\
        .select("*")\
        .eq("org_id", org_id)\
        .eq("user_id", user.id)\
        .execute()
    
    if not result.data:
        raise HTTPException(status_code=403, detail="您不是此組織的成員")
    
    return org_id
